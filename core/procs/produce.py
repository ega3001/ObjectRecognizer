import logging
from multiprocessing import Queue

from core.logger import getWorkerLogger
from core.kafka import Producer
from core.config import AppConfig


def ProduceProc(inQ: Queue, logQ: Queue):
    logger = getWorkerLogger("PRODUCER", logQ)
    logger.setLevel(logging.DEBUG)
    producer = Producer(AppConfig.Broker)

    logger.info("STARTED PRODUCE")
    while True:
        dm = inQ.get()
        producer.produce(
            topic=AppConfig.DetectionsTopic,
            value=dm.to_bytes(),
            on_delivery=lambda err, msg: logger.debug(
                f"DELIVERED: ERR{err};MSG:{msg}")
        )
