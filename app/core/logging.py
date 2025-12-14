import logging
from datetime import datetime
from zoneinfo import ZoneInfo  # Python 3.9+


class TZFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None, tz: str = "Europe/Athens"):
        super().__init__(fmt, datefmt)
        self.tz = ZoneInfo(tz)

    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created, tz=self.tz)
        if datefmt:
            return dt.strftime(datefmt)
        return dt.isoformat()


def setup_logging():
    logger = logging.getLogger("fastapi_app")
    logger.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    formatter = TZFormatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        tz="Europe/Athens",
    )
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger


logger = setup_logging()
