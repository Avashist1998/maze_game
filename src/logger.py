"""Maze Game Logger definition."""
from typing import Final
from logging import INFO, DEBUG, getLogger, FileHandler, StreamHandler, Formatter, Logger

from src.config import get_config


def init_logger(name: str) -> Logger:
    """Initialize the module logger."""
    config = get_config()
    print(config)
    logger: Final = getLogger(name)
    logger.setLevel(INFO)
    if config.DEBUG:
        logger.setLevel(DEBUG)

    # create file handler which logs even debug messages
    file_handler = FileHandler(config.LOG_FILE)
    file_handler.setLevel(INFO)
    if config.DEBUG:
        file_handler.setLevel(DEBUG)
    # create console handler with a higher log level
    console_handler = StreamHandler()
    console_handler.setLevel(INFO)
    if config.DEBUG:
        console_handler.setLevel(DEBUG)
    # create formatter and add it to the handlers
    formatter = Formatter(config.LOG_FORMAT, datefmt=config.LOG_DATE_FORMAT)

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # add the handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
