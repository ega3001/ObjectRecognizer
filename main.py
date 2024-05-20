import logging
from multiprocessing import Queue, Process
from time import sleep

from core.config import AppConfig
from core.logger import getWorkerLogger
from core.procs import ConsumeProc, ProduceProc, DetectProc, LoggingProc


def main():
    framesQueue = Queue(AppConfig.QueueLimit)
    detectionQueue = Queue()
    logQueue = Queue()

    procs = [
        Process(target=ConsumeProc, args=(framesQueue, logQueue), daemon=True),
        Process(target=ProduceProc, args=(detectionQueue,  logQueue)),
        Process(target=LoggingProc, args=(logQueue,))
    ]
    for _ in range(AppConfig.ai.workers):
        procs.append(
            Process(target=DetectProc, args=(
                framesQueue, detectionQueue, logQueue)),
        )

    logger = getWorkerLogger("MAIN", logQueue)
    logger.setLevel(logging.DEBUG)

    logger.info("STARTING SUBPROCESSES...")
    try:
        for p in procs:
            p.start()

        while True:
            if any([not p.is_alive() for p in procs]):
                logger.debug("HEALTHCHECK: FAIL")
                break
            logger.debug("HEALTHCHECK: OK")
            sleep(AppConfig.HealthCheckTimeout)
    finally:
        logger.info("STOPPING SUBPROCESSES...")
        sleep(1)
        for p in procs:
            p.terminate()
        for p in procs:
            p.join()
        for p in procs:
            p.close()


if __name__ == "__main__":
    main()
