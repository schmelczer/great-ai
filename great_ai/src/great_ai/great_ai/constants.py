from pathlib import Path

from great_ai.large_file import LargeFileLocal, LargeFileMongo, LargeFileS3

ENV_VAR_KEY = "ENVIRONMENT"
PRODUCTION_KEY = "production"
DEFAULT_TRACING_DB_FILENAME = "tracing_database.json"
DASHBOARD_PATH = "/dashboard"

DEFAULT_LARGE_FILE_CONFIG_PATHS = {
    LargeFileLocal: None,
    LargeFileMongo: Path("mongodb.ini"),
    LargeFileS3: Path("s3.ini"),
}

GITHUB_LINK = "https://github.com/ScoutinScience/great-ai"
