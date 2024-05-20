import logging
from logging.handlers import QueueHandler
from multiprocessing import Queue


def getWorkerLogger(name: str, queue: Queue) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.addHandler(QueueHandler(queue))

    return logger
