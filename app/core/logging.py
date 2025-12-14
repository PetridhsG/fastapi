import logging
from datetime import datetime
from zoneinfo import ZoneInfo

TZ = ZoneInfo("Europe/Athens")


class TZFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created, tz=TZ)
        if datefmt:
            return dt.strftime(datefmt)
        return dt.isoformat()

    def format(self, record):
        time_str = self.formatTime(record, self.datefmt)
        return (
            f"{record.levelname} - {time_str} - {record.name} - {record.getMessage()}"
        )


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {"()": TZFormatter, "datefmt": "%Y-%m-%d %H:%M:%S"},
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": "INFO",
        },
    },
    "root": {"handlers": ["console"], "level": "INFO"},  # Root logger prints everything
    "loggers": {
        "uvicorn.error": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
            "formatter": "default",
        },
        "fastapi_app": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
            "formatter": "default",
        },
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("fastapi_app")
