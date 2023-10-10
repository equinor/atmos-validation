import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Callable, Optional

LOG_FILE_NAME = (
    f"atmos-validation-library-debug-log-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
)
LOG_DIRECTORY = Path.joinpath(Path(os.getcwd()), "atmos-validation-logs")
LOG_ENTRY_FORMAT: str = (
    "[%(asctime)s][%(filename)s][%(lineno)d][%(levelname)s] %(message)s"
)
LOG_TIME_FORMAT = "%H:%M:%S"
VALIDATION_LOGGER: str = "validation-logger"


def setup_logger(write_to_file: bool = False) -> logging.Logger:
    log_formatter = logging.Formatter(LOG_ENTRY_FORMAT, LOG_TIME_FORMAT)
    root_logger = logging.getLogger(VALIDATION_LOGGER)
    root_logger.setLevel(logging.DEBUG)
    if write_to_file:
        if not os.path.exists(LOG_DIRECTORY):
            os.makedirs(LOG_DIRECTORY)
        file_handler = logging.FileHandler(f"{LOG_DIRECTORY}/{LOG_FILE_NAME}.log")
        file_handler.setFormatter(log_formatter)
        file_handler.setLevel(logging.DEBUG)
        root_logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(logging.INFO)
    root_logger.addHandler(console_handler)

    return root_logger


_default_logger = setup_logger()


# pylint: disable=too-few-public-methods
class LogWrapper:
    def __init__(self):
        self._log: Optional[logging.Logger] = None
        self.debug: Callable[..., None] = lambda _: None  # type:ignore
        self.info: Callable[..., None] = lambda _: None  # type:ignore
        self.warning: Callable[..., None] = lambda _: None  # type:ignore
        self.error: Callable[..., None] = lambda _: None  # type:ignore
        self.exception: Callable[..., None] = lambda _: None  # type:ignore

    def create_or_update_logger(self, injected_logger: Optional[logging.Logger] = None):
        if self._log is not None and self._log is _default_logger:
            # Cleanup old logger
            old_handlers = _default_logger.handlers[:]
            for handler in old_handlers:
                self._log.removeHandler(handler)
                handler.close()
            self._log = setup_logger()

        self._log = injected_logger if injected_logger else _default_logger
        self.debug = self._log.debug
        self.info = self._log.info
        self.warning = self._log.warning
        self.error = self._log.error
        self.exception = self._log.exception
        if injected_logger is None:
            self.debug("Validation library log initialized")
        else:
            self.info("Using injected logger for validation library")


log = LogWrapper()
