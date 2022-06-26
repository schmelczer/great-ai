#!/usr/bin/env python3

import logging
import re
from importlib import import_module, reload
from pathlib import Path
from threading import Event
from typing import Optional

import uvicorn
from uvicorn._subprocess import get_subprocess
from uvicorn.config import LOGGING_CONFIG, Config
from uvicorn.supervisors.basereload import BaseReload
from watchdog.events import FileSystemEvent, PatternMatchingEventHandler
from watchdog.observers import Observer

from .great_ai.constants import SERVER_NAME
from .great_ai.context import _is_in_production_mode
from .great_ai.deploy import GreatAI
from .great_ai.exceptions import ArgumentValidationError, MissingArgumentError
from .parse_arguments import parse_arguments
from .utilities import get_logger

logger = get_logger(SERVER_NAME)


GREAT_AI_LOGGING_CONFIG = {
    **LOGGING_CONFIG,
    "formatters": {
        "default": {
            "()": "great_ai.logger.CustomFormatter",
            "fmt": "%(asctime)s | %(levelname)8s | %(message)s",
        },
        "access": {
            "()": "great_ai.logger.CustomFormatter",
            "fmt": "%(asctime)s | %(levelname)8s | %(message)s",  # noqa: E501
        },
    },
}


def main() -> None:
    args = parse_arguments()
    should_auto_reload = not _is_in_production_mode(logger=None)

    if args.workers > 1 and should_auto_reload:
        raise ArgumentValidationError(
            "Cannot use auto-reload with multiple workers: set the `--workers=1` CLI argument,"
            + "or set the ENVIRONMENT environment variable to `production`."
        )

    common_config = dict(
        host=args.host,
        port=args.port,
        timeout_keep_alive=args.timeout_keep_alive,
        workers=args.workers,
        server_header=False,
        reload=False,
        log_config=GREAT_AI_LOGGING_CONFIG,
    )

    if not should_auto_reload:
        file_name = get_script_name(args.file_name)
        app = find_app(file_name)

        logger.info(f"Starting uvicorn server with app={app}")

        config = Config(app, **common_config)
        socket = config.bind_socket()
        server = GreatAIReload(
            config, target=uvicorn.Server(config=config).run, sockets=[socket]
        )

        server.startup()
        try:
            Event().wait()
        finally:
            server.shutdown()
            if args.file_name.endswith(".ipynb"):
                Path(get_script_name_of_notebook(args.file_name)).unlink(
                    missing_ok=True
                )
    else:

        class EventHandler(PatternMatchingEventHandler):
            def __init__(self) -> None:
                super().__init__(
                    patterns=["*.py", "*.ipynb"], ignore_patterns=["__*.py"]
                )
                self.server: Optional[GreatAIReload] = None
                self.restart()

            def on_closed(self, event: FileSystemEvent) -> None:
                logger.warning(f"File {event.src_path} has triggered a restart")
                self.restart()

            def restart(self) -> None:
                file_name = get_script_name(args.file_name)
                app = find_app(file_name)
                if app is None:
                    logger.warning("Auto-reloading skipped")
                    return

                self.stop_server()

                config = Config(app, **common_config)
                socket = config.bind_socket()
                self.server = GreatAIReload(
                    config, target=uvicorn.Server(config=config).run, sockets=[socket]
                )
                self.server.startup()

            def stop_server(self) -> None:
                if self.server:
                    self.server.shutdown()

        restart_handler = EventHandler()
        observer = Observer()
        observer.schedule(restart_handler, path=".", recursive=True)
        observer.start()

        try:
            Event().wait()
        finally:
            observer.stop()
            restart_handler.stop_server()
            if args.file_name.endswith(".ipynb"):
                Path(get_script_name_of_notebook(args.file_name)).unlink(
                    missing_ok=True
                )
            observer.join()


def get_script_name(file_name_argument: str) -> str:
    if file_name_argument.endswith(".ipynb"):
        logger.info("Converting notebook to Python script")
        from nbconvert import PythonExporter

        exporter = PythonExporter()
        content, _ = exporter.from_filename(file_name_argument)
        file_name_argument = get_script_name_of_notebook(file_name_argument)

        with open(file_name_argument, "w", encoding="utf-8") as f:
            f.write(content)

    return re.sub(r"\.(py|ipynb)$", "", file_name_argument)


def get_script_name_of_notebook(notebook_name: str) -> str:
    base_name = re.sub(r"\.ipynb$", "", notebook_name)
    return f"__{base_name}__.py"


module = None


def find_app(file_name: str) -> Optional[str]:
    global module

    logging.disable(logging.CRITICAL)
    try:
        if module is None:
            module = import_module(file_name)
        else:
            module = reload(module)
    except Exception:
        logging.disable(logging.NOTSET)
        logger.exception("Could not load file because of an exception: fix your code")
        return None
    finally:
        logging.disable(logging.NOTSET)

    for name, value in module.__dict__.items():
        if isinstance(value, GreatAI):
            app_name = name

    if app_name:
        logger.info(f"Found `{app_name}` to be the GreatAI app ")
    else:
        raise MissingArgumentError(
            "GreatAI app could not be found, make sure to use `@GreatAI.deploy` on your prediction function"
        )

    return f"{file_name}:{app_name}.app"


class GreatAIReload(BaseReload):
    def startup(self) -> None:
        self.process = get_subprocess(
            config=self.config, target=self.target, sockets=self.sockets
        )
        self.process.start()

    def shutdown(self) -> None:
        self.process.terminate()
        self.process.join()

        for sock in self.sockets:
            sock.close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()
    except Exception as e:
        logger.error(e)
