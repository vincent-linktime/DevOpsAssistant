#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import inspect
import logging
import os
import threading
from pathlib import Path
from typing import Dict, Optional, Union

thread_local = threading.local()

class DevOpsAILogger:
    """This is an event logger wrapper.

    Args:
        name (str): The name of the logger.

    """

    # todo: the value is DevOpsAILogger, need to figure out how to type hint
    __instances: Dict[str, "DevOpsAILogger"] = {}

    global_default_level: str = "INFO"

    @staticmethod
    def set_global_default_level(level: str) -> None:
        """Set the global default logging level.

        Args:
            level (logging._Level): The level to be set.
        """
        level = level.upper()
        DevOpsAILogger.global_default_level = level
        for logger in DevOpsAILogger.__instances.values():
            logger.set_level(level)

    @staticmethod
    def get_thread_local_instance() -> "DevOpsAILogger":
        if hasattr(thread_local, "logger"):
            return thread_local.logger

        thread_name = f"{threading.current_thread().name}-{threading.get_native_id()}"
        logger = DevOpsAILogger.get_instance(name=thread_name)
        thread_local.logger = logger
        return logger

    @staticmethod
    def get_instance(name: str = "data", config: dict = {}) -> "DevOpsAILogger":
        """Get the unique single logger instance based on name.

        Args:
            name (str): The name of the logger.

        Returns:
            DevOpsAILogger: A DevOpsAILogger object
        """
        if name in DevOpsAILogger.__instances:
            return DevOpsAILogger.__instances[name]
        else:
            logger = DevOpsAILogger(name=name)
            log_dir = config["logging"]["log_dir"]
            log_file = config["logging"]["log_file"]
            log_level = config["logging"]["log_level"]
            logger.log_to_dir(dir=log_dir, filename=log_file, level=log_level)
            return logger

    def get_default_formatter(self) -> logging.Formatter:
        """Get the default formatter with no rich formatting.

        Returns:
            logging.Formatter: The default formatter.
        """
        fmt = "[%(asctime)s] %(levelname)s %(message)s"
        datefmt = "%d/%m/%y %H:%M:%S"
        formatter = logging.Formatter(fmt, datefmt)
        return formatter

    def __init__(self, name):
        if name in DevOpsAILogger.__instances:
            raise Exception(
                "Logger with the same name exists, you should use src.logging.get_logger"
            )
        else:
            handler = None

            try:
                from rich.logging import Console, RichHandler

                formatter = logging.Formatter("%(message)s")
                handler = RichHandler(
                    show_path=False,
                    markup=True,
                    show_level=True,
                    console=Console(width=150),  # 250 is the width of the terminal
                    rich_tracebacks=True,
                )
                handler.setFormatter(formatter)
            except ImportError:
                handler = logging.StreamHandler()
                handler.setFormatter(self.get_default_formatter())

            self._name = name
            self._logger = logging.getLogger(name)
            self._pid = os.getpid()
            self._tid = threading.get_native_id()
            self._default_handler = handler
            self.set_level(DevOpsAILogger.global_default_level)
            if handler is not None:
                self._logger.addHandler(handler)
            self._logger.propagate = False
            self._file_handler = None

            DevOpsAILogger.__instances[name] = self

    @staticmethod
    def __get_call_info():
        stack = inspect.stack()

        # stack[1] gives previous function ('info' in our case)
        # stack[2] gives before previous function and so on

        fn = stack[2][1]
        fn = fn.split("/")[-1]
        ln = stack[2][2]
        func = stack[2][3]

        return fn, ln, func

    @staticmethod
    def _check_valid_logging_level(level: str):
        assert level in [
            "INFO",
            "DEBUG",
            "WARNING",
            "ERROR",
        ], "found invalid logging level"

    def set_level(self, level: str) -> None:
        """Set the logging level

        Args:
            level (Union[int, str]): Can only be INFO, DEBUG, WARNING and ERROR.
        """
        level = level.upper()
        self._check_valid_logging_level(level)

        self.level = level
        self._logger.setLevel(getattr(logging, level))

    def get_level(self) -> str:
        """Get the logging level"""
        return self.level

    def log_to_file(
        self, file: Union[str, Path], level: Optional[str] = None, mode: str = "a"
    ) -> logging.FileHandler:
        """Save the logs to a file

        Args:
            file (A string or pathlib.Path object): The file to save the log.
            level (str): Can only be INFO, DEBUG, WARNING and ERROR. If None, use current logger level.
            mode (str): The mode to write log into the file.
        """
        assert isinstance(
            file, (str, Path)
        ), f"expected argument path to be type str or Path, but got {type(file)}"
        if isinstance(file, str):
            file = Path(file)
        return self.log_to_dir(file.parent, level, mode, file.name)

    def log_to_dir(
        self,
        dir: Union[str, Path],
        level: Optional[str] = None,
        mode: str = "a",
        filename: str = "data.log",
    ) -> logging.FileHandler:
        """Save the logs to a dir

        Args:
            dir (A string or pathlib.Path object): The directory to save the log.
            mode (str): The mode to write log into the file.
            level (str): Can only be INFO, DEBUG, WARNING and ERROR. If None, use current logger level.
            filename (str): a log filename, default is 'data.log'.
        """
        assert isinstance(
            dir, (str, Path)
        ), f"expected argument path to be type str or Path, but got {type(dir)}"
        if level is None:
            log_level = self.level
        else:
            log_level = level.upper()

        self._check_valid_logging_level(log_level)

        if isinstance(dir, str):
            dir = Path(dir)

        # create log directory
        dir.mkdir(parents=True, exist_ok=True)
        log_file = dir.joinpath(filename)

        # add file handler
        file_handler = logging.FileHandler(log_file, mode)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(self.get_default_formatter())
        self._logger.addHandler(file_handler)
        self._file_handler = file_handler
        return file_handler

    def get_file_handler(self) -> Optional[logging.FileHandler]:
        """Get the file handler of the logger.

        Returns:
            logging.FileHandler: The file handler of the logger.
        """
        return self._file_handler

    def remove_file_handler(self) -> None:
        if self._file_handler is not None:
            self._logger.removeHandler(self._file_handler)
            self._file_handler = None
        else:
            raise RuntimeError(
                "Trying to remove file handler while none is attached to the logger."
            )

    def _log(self, level, message: str) -> None:
        getattr(self._logger, level)(message)

    def info(self, message: str) -> None:
        """Log an info message.

        Args:
            message (str): The message to be logged.
        """
        message_prefix = "{}:{} {}".format(*self.__get_call_info())
        self._log("info", f"[{self._pid}-{self._tid}] {message} [{message_prefix}]")

    def warning(self, message: str) -> None:
        """Log a warning message.

        Args:
            message (str): The message to be logged.
        """
        message_prefix = "{}:{} {}".format(*self.__get_call_info())
        self._log("warning", f"[{self._pid}-{self._tid}] {message} [{message_prefix}]")

    def debug(self, message: str) -> None:
        """Log a debug message.

        Args:
            message (str): The message to be logged.
        """
        message_prefix = "{}:{} {}".format(*self.__get_call_info())
        self._log("debug", f"[{self._pid}-{self._tid}] {message} [{message_prefix}]")

    def error(self, message: str) -> None:
        """Log an error message.

        Args:
            message (str): The message to be logged.
        """
        message_prefix = "{}:{} {}".format(*self.__get_call_info())
        self._log("error", f"[{self._pid}-{self._tid}] {message} [{message_prefix}]")

    def noop(self, message: str) -> None:
        """No-op, for place holders and temporary logging.

        Args:
            message (str): The message to be logged.
        """
        # TODO: using an env variable to enable this most verbose logging
        # but we do not want to check the environment every time we call this function
        return


logger = DevOpsAILogger.get_thread_local_instance