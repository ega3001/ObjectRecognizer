import logging
import copy
from multiprocessing import Queue

from core.logger import getWorkerLogger
from core.kafka import Consumer, FrameMessage, Location
from core.config import AppConfig


def ConsumeProc(outQ: Queue, logQ: Queue):
    logger = getWorkerLogger('CONSUME', logQ)
    logger.setLevel(logging.DEBUG)
    kc = Consumer(AppConfig.Broker, AppConfig.ConsumeGroup)
    logger.info("STARTED CONSUME")
    for msg in kc.consume([AppConfig.FramesTopic]):
        logger.debug(
            f"FROM MSG: {msg.partition()}; {msg.offset()}; {msg.headers()}; {msg.timestamp()}; {len(msg.value())}")
        fm = FrameMessage.from_kafka(msg)
        location = Location(
            offset=msg.offset(),
            partition=msg.partition(),
            topic=msg.topic()
        )
        outQ.put((copy.copy(fm), location, msg.timestamp()[1]))
