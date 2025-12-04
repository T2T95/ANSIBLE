import logging
import sys


def setup_logger(
    name: str = "mla", level: int = logging.INFO, debug: bool = False
) -> logging.Logger:
    """Configure and return a logger instance.

    Args:
        name: Logger name
        level: Logging level (default: INFO)
        debug: Enable debug mode (default: False)

    Returns:
        Configured logger instance
    """
    if debug:
        level = logging.DEBUG

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()

    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)

    # Create formatter with timestamp
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def get_logger(name: str = "mla") -> logging.Logger:
    """Get logger instance.

    Args:
        name: Logger name

    Returns:
        Logger instance
    """
    return logging.getLogger(name)
