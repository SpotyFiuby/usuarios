import logging


def create_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    StreamHandler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(module)s - %(funcName)s - %(levelname)s - %(message)s"
    )
    StreamHandler.setFormatter(formatter)
    logger.addHandler(StreamHandler)  # Exporting logs to the screen

    return logger
