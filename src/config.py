"""Defines the config class for the maze game."""
import os


class Config:
    """Defines the config class for the maze game."""

    DEBUG = False
    TWITCH_MODE = False
    APP_NAME = "Maze Game"
    APP_VERSION = "1.0.0"
    APP_DESCRIPTION = "A maze game."
    APP_AUTHOR = "The Maze Game Team"
    APP_CONFIG = "CONFIG"
    LOG_LEVEL = "INFO"
    LOG_FILE = "maze_game.log"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class BaseConfig(Config):
    """Defines the base config class for the maze game."""

    TWITCH_MODE = False
    APP_CONFIG = "BASE_CONFIG"


class TwitchConfig(Config):
    """Defines the twitch config class for the maze game."""

    APP_CONFIG = "TWITCH_CONFIG"
    TWITCH_MODE = os.environ.get("TWITCH_MODE", "False") == "True"
    TWITCH_CHANNEL = os.environ.get("TWITCH_CHANNEL", "")
    TWITCH_USERNAME = os.environ.get("TWITCH_USERNAME", "")
    TWITCH_OAUTH_TOKEN = os.environ.get("TWITCH_OAUTH_TOKEN", "")


def get_config() -> Config:
    """Returns the config object."""
    if TwitchConfig.TWITCH_MODE:
        return TwitchConfig    # type: ignore
    return BaseConfig    # type: ignore
