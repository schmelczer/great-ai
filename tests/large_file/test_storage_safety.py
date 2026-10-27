import io
import multiprocessing as mp
import tarfile
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Iterator
from unittest.mock import MagicMock, patch

import boto3
import pytest
from boto3.s3.transfer import TransferConfig
from botocore.stub import Stubber
from great_ai.large_file import (
    LargeFileBase,
    LargeFileLocal,
    LargeFileMongo,
    LargeFileS3,
)
from pymongo.errors import DuplicateKeyError


@pytest.fixture(autouse=True)
def storage(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    for implementation in (LargeFileBase, LargeFileLocal):
        monkeypatch.setattr(implementation, "cache_path", tmp_path / "cache")
        monkeypatch.setattr(implementation, "max_cache_size", None)
    yield


def test_configured_cache_directory_is_created(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(LargeFileLocal, "cache_path", tmp_path / "custom-cache")
    with LargeFileLocal("model", "w") as file:
        file.write("weights")
    assert LargeFileLocal("model").get().read_text() == "weights"


def test_unrelated_cache_entries_are_ignored() -> None:
    LargeFileLocal.cache_path.mkdir(parents=True)
    (LargeFileLocal.cache_path / "model-unrelated").write_text("unrelated")
    (LargeFileLocal.cache_path / "model-0").write_text("weights")
    assert LargeFileLocal("model").get().read_text() == "weights"


@pytest.mark.parametrize("operation", ["delete", "prune"])
def test_cached_directories_can_be_removed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, operation: str
) -> None:
    source = tmp_path / "source"
    source.mkdir()
    (source / "weights").write_text("weights")
    LargeFileLocal("model", "w").push(source)
    reader = LargeFileLocal("model")
    cached = reader.get()
    if operation == "delete":
        reader.delete()
    else:
        monkeypatch.setattr(LargeFileLocal, "max_cache_size", "0")
        reader.clean_up()
    assert not cached.exists()


def test_cache_quota_counts_directory_contents(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = tmp_path / "source"
    source.mkdir()
    (source / "weights").write_bytes(b"x" * 100_000)
    monkeypatch.setattr(LargeFileLocal, "max_cache_size", "1 KB")
    LargeFileLocal("model", "w").push(source)
    assert not (LargeFileLocal.cache_path / "model-0").exists()


def test_failed_write_removes_temporary_file() -> None:
    temporary = None
    try:
        with pytest.raises(ValueError, match="failed"):
            with LargeFileLocal("model", "w") as file:
                temporary = Path(file.name)
                file.write("unfinished")
                raise ValueError("failed")
        assert temporary is not None
        assert not temporary.exists()
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def test_evicted_remote_model_is_downloaded_again() -> None:
    backend = MagicMock()
    backend.list_objects_v2.return_value = {"Contents": [{"Key": "model/0"}]}
    downloads = []

    def download(
        self: LargeFileS3, remote_path: Any, local_path: Path, hide_progress: bool
    ) -> None:
        downloads.append(remote_path)
        with tarfile.open(local_path, "w:gz") as archive:
            payload = b"remote weights"
            member = tarfile.TarInfo("model-0")
            member.size = len(payload)
            archive.addfile(member, io.BytesIO(payload))

    with (
        patch.object(LargeFileS3, "_client", backend),
        patch.object(LargeFileS3, "_download", download),
    ):
        reader = LargeFileS3("model")
        cached = reader.get()
        cached.unlink()
        assert reader.get().read_text() == "remote weights"
    assert downloads == ["model/0", "model/0"]


def test_upload_refreshes_available_versions() -> None:
    writer = LargeFileLocal("model", "w")
    with writer as file:
        file.write("weights")
    assert writer.versions_pretty == "0"
    assert writer.get().read_text() == "weights"


def test_retention_counts_the_new_version() -> None:
    for version in range(3):
        with LargeFileLocal("model", "w", keep_last_n=1) as file:
            file.write(str(version))
    reader = LargeFileLocal("model")
    assert reader.versions_pretty == "2"
    assert reader.get().read_text() == "2"


@pytest.mark.parametrize(
    "implementation", [LargeFileLocal, LargeFileS3, LargeFileMongo]
)
def test_negative_retention_is_rejected_before_storage_access(
    implementation: Any,
) -> None:
    with LargeFileLocal("preserved", "w") as file:
        file.write("weights")
    with pytest.raises(ValueError, match="keep_last_n must be non-negative"):
        implementation("preserved", "w", keep_last_n=-1)
    assert LargeFileLocal("preserved").get().read_text() == "weights"


def write_model(root: str, value: str, barrier: Any) -> None:
    LargeFileBase.cache_path = LargeFileLocal.cache_path = Path(root)
    LargeFileBase.max_cache_size = LargeFileLocal.max_cache_size = None
    writer = LargeFileLocal("model", "w")
    barrier.wait(timeout=10)
    with writer as file:
        file.write(value)


def test_overlapping_local_writers_preserve_both_versions() -> None:
    first = LargeFileLocal("model", "w")
    second = LargeFileLocal("model", "w")
    for writer, value in [(first, "first"), (second, "second")]:
        with writer as file:
            file.write(value)
    assert first.version == 0
    assert second.version == 1
    assert LargeFileLocal("model", version=0).get().read_text() == "first"
    assert LargeFileLocal("model", version=1).get().read_text() == "second"


def test_concurrent_processes_preserve_both_versions(tmp_path: Path) -> None:
    ctx = mp.get_context("spawn")
    barrier = ctx.Barrier(2)
    processes = [
        ctx.Process(target=write_model, args=(str(tmp_path / "cache"), value, barrier))
        for value in ("first", "second")
    ]
    try:
        for process in processes:
            process.start()
        for process in processes:
            process.join(timeout=15)
            assert process.exitcode == 0
    finally:
        for process in processes:
            if process.is_alive():
                process.kill()
                process.join()
            process.close()
    assert {LargeFileLocal("model", version=v).get().read_text() for v in (0, 1)} == {
        "first",
        "second",
    }


def test_uploading_cached_directory_preserves_source(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    (source / "weights").write_text("model weights")
    LargeFileLocal("model", "w").push(source)
    reader = LargeFileLocal("model")
    cached = reader.get()
    reader.push(cached)
    assert reader.version == 1
    assert (cached / "weights").read_text() == "model weights"
    assert (
        LargeFileLocal("model", version=1).get() / "weights"
    ).read_text() == "model weights"


def test_gridfs_matches_only_exact_model_names() -> None:
    files = [
        SimpleNamespace(name=name, _id=name, length=1)
        for name in ("model_0", "model_other_9", "other_model_10", "model_1_backup")
    ]
    backend = MagicMock()
    backend.find.side_effect = lambda query: [
        file for file in files if query["filename"].search(file.name)
    ]
    with patch.object(LargeFileMongo, "_client", backend):
        reader = LargeFileMongo("model")
    assert reader.version == 0
    assert [instance.name for instance in reader._instances] == ["model"]


def test_remote_cache_is_separate_from_local_cache() -> None:
    with LargeFileLocal("model", "w") as file:
        file.write("local weights")
    local_path = LargeFileLocal("model").get()
    backend = MagicMock()
    backend.list_objects_v2.return_value = {"Contents": [{"Key": "model/0"}]}

    def download(
        self: LargeFileS3, remote_path: Any, local_path: Path, hide_progress: bool
    ) -> None:
        with tarfile.open(local_path, "w:gz") as archive:
            data = b"remote weights"
            info = tarfile.TarInfo("model-0")
            info.size = len(data)
            archive.addfile(info, io.BytesIO(data))

    with (
        patch.object(LargeFileS3, "_client", backend),
        patch.object(LargeFileS3, "_download", download),
    ):
        remote_path = LargeFileS3("model").get()
    assert remote_path != local_path
    assert remote_path.read_text() == "remote weights"
    assert local_path.read_text() == "local weights"


def test_cache_identity_includes_storage_configuration(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    backend = MagicMock()
    backend.list_objects_v2.return_value = {"Contents": [{"Key": "model/0"}]}
    monkeypatch.setattr(LargeFileS3, "bucket_name", "first")
    with patch.object(LargeFileS3, "_client", backend):
        first = LargeFileS3("model")
        monkeypatch.setattr(LargeFileS3, "bucket_name", "second")
        second = LargeFileS3("model")
        monkeypatch.setattr(
            LargeFileS3, "endpoint_url", "https://another-store.example"
        )
        third = LargeFileS3("model")
    assert len({first._cache_name, second._cache_name, third._cache_name}) == 3
    assert first.bucket_name == "first"
    assert second.bucket_name == "second"
    assert second.endpoint_url != third.endpoint_url


def test_s3_follows_every_listing_page() -> None:
    backend = MagicMock()
    backend.list_objects_v2.side_effect = [
        {
            "Contents": [{"Key": "model/0"}, {"Key": "model-other/99"}],
            "IsTruncated": True,
            "NextContinuationToken": "next",
        },
        {
            "Contents": [
                {"Key": "model/9"},
                {"Key": "model/backup"},
                {"Key": "model/9/extra"},
            ]
        },
    ]
    with patch.object(LargeFileS3, "_client", backend):
        reader = LargeFileS3("model")
    assert reader.version == 9
    assert [instance.version for instance in reader._instances] == [0, 9]
    assert backend.list_objects_v2.call_args_list[0].kwargs["Prefix"] == "model/"
    assert (
        backend.list_objects_v2.call_args_list[1].kwargs["ContinuationToken"] == "next"
    )


@pytest.mark.parametrize("multipart", [False, True])
@pytest.mark.parametrize("conflict", [False, True])
def test_s3_commits_are_conditional(
    tmp_path: Path, multipart: bool, conflict: bool
) -> None:
    client = boto3.client(
        "s3",
        region_name="us-east-1",
        aws_access_key_id="test",
        aws_secret_access_key="test",
    )
    writer = LargeFileS3.__new__(LargeFileS3)
    writer._client = client
    writer.bucket_name = "models"
    writer._name = "model"
    writer._version = 0
    archive = tmp_path / "archive"
    archive.write_bytes(b"model weights")
    operation = "CompleteMultipartUpload" if multipart else "PutObject"
    headers = []

    def capture(model: Any, params: Any, **kwargs: Any) -> None:
        if model.name == operation:
            headers.append(params["headers"].get("If-None-Match"))

    client.meta.events.register_first("before-call.*.*", capture)
    config = TransferConfig(
        multipart_threshold=1 if multipart else 1024,
        use_threads=False,
        preferred_transfer_client="classic",
    )
    with (
        Stubber(client) as stubber,
        patch(
            "great_ai.large_file.large_file.large_file_s3.TransferConfig",
            return_value=config,
        ),
    ):
        if multipart:
            stubber.add_response("create_multipart_upload", {"UploadId": "upload"})
            stubber.add_response("upload_part", {"ETag": '"part"'})
        commit = "complete_multipart_upload" if multipart else "put_object"
        if conflict:
            stubber.add_client_error(
                commit, service_error_code="PreconditionFailed", http_status_code=412
            )
            if multipart:
                stubber.add_response("abort_multipart_upload", {})
            with pytest.raises(FileExistsError, match="another writer"):
                writer._upload(archive, hide_progress=True)
        else:
            stubber.add_response(commit, {"ETag": '"model"'})
            writer._upload(archive, hide_progress=True)
        stubber.assert_no_pending_responses()
    assert headers == ["*"]
    client.close()


def test_gridfs_rejects_conflicting_versions_and_aborts(tmp_path: Path) -> None:
    backend = MagicMock()
    stream = backend.open_upload_stream.return_value
    stream.__enter__.return_value = stream
    stream.__exit__.side_effect = DuplicateKeyError("duplicate filename")
    database = MagicMock()
    source = tmp_path / "weights"
    source.write_text("weights")
    with (
        patch.object(LargeFileMongo, "_client", backend),
        patch.object(LargeFileMongo, "_database", database),
    ):
        writer = LargeFileMongo("model", "w")
        with pytest.raises(FileExistsError, match="another writer"):
            writer.push(source)
    database.fs.files.create_index.assert_called_once_with(
        "filename",
        name="great_ai_unique_version",
        unique=True,
        partialFilterExpression={"metadata.great_ai_version": True},
    )
    backend.open_upload_stream.assert_called_once_with(
        "model_0", metadata={"great_ai_version": True}
    )
    stream.abort.assert_called_once()
    assert not (writer.cache_path / writer._cache_name).exists()
