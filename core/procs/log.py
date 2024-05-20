import logging
from multiprocessing import Queue


def LoggingProc(inQ: Queue):
    logger = logging.getLogger('app')
    logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(processName)-10s %(name)s %(levelname)-8s %(message)s'))
    logger.addHandler(console_handler)

    logger.info(f'Logger process running.')
    while True:
        message = inQ.get()
        if message is None:
            logger.info(f'Logger process shutting down.')
            break
        logger.handle(message)
