import logging
import os
from logging.handlers import RotatingFileHandler

_LOGGERS = {}

def get_logger(name: str = "drinksrobot", log_dir: str = None, level: int = logging.INFO) -> logging.Logger:
    global _LOGGERS
    if name in _LOGGERS:
        return _LOGGERS[name]

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Avoid duplicate handlers on reload
    if logger.handlers:
        _LOGGERS[name] = logger
        return logger

    # Determine log directory (default to project root / logs)
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    log_dir = log_dir or os.path.join(base_dir, "logs")
    os.makedirs(log_dir, exist_ok=True)

    file_handler = RotatingFileHandler(os.path.join(log_dir, "app.log"), maxBytes=1_000_000, backupCount=5)
    file_handler.setLevel(level)
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s - %(message)s")
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    _LOGGERS[name] = logger
    return logger
