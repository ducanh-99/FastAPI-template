import logging
from typing import Union, Text


def get_logger(name: Union[Text, str]) -> logging.Logger:
    logging.basicConfig(
        format="%(asctime)s, %(levelname)-8s | %(filename)-23s:%(lineno)-4s | %(threadName)15s: %(message)s",
        datefmt="%Y-%m-%d, %H:%M:%S",
        level=logging.INFO
    )

    return logging.getLogger(name)
