"""Maze Game Logger definition."""
from typing import Final
from logging import INFO, getLogger, FileHandler, StreamHandler, Formatter, Logger


def init_logger(name: str) -> Logger:
    """Initialize the module logger."""

    logger: Final = getLogger(name)
    logger.setLevel(INFO)

    # create file handler which logs even debug messages
    file_handler = FileHandler('run_logs.log')
    file_handler.setLevel(INFO)
    # create console handler with a higher log level
    console_handler = StreamHandler()
    console_handler.setLevel(INFO)
    # create formatter and add it to the handlers
    formatter = Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # add the handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
