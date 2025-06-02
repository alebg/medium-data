"""
Util to quickly configure a logger.
"""

import logging

def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Get a configured logger.

    Args:
        name (str): Name of the logger.
        level (int): Logging level. Defaults to logging.INFO.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create console handler
    ch = logging.StreamHandler()
    ch.setLevel(level)

    # Create formatter and add it to the handler
    datefmt = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt)

    ch.setFormatter(formatter)

    # Add the handler to the logger
    if not logger.hasHandlers():
        logger.addHandler(ch)

    return logger