import logging
import copy
from datetime import datetime
from multiprocessing import Queue

from core.logger import getWorkerLogger
from core.kafka import DetectionMessage, Frame, Object
from core.recognizer import initRecognizer


def DetectProc(inQ: Queue, outQ: Queue, logQ: Queue):
    logger = getWorkerLogger("DETECTOR", logQ)
    logger.setLevel(logging.DEBUG)
    recognizer = initRecognizer()

    logger.info("STARTED DETECT")
    while True:
        (fm, loc, ts) = inQ.get()
        logger.debug(f"GOT: {fm.producer}\n VALUE: {len(fm.data)}")
        try:
            data = recognizer.score(fm.data)
            if not len(data):
                logger.debug(f"NO DATA: {loc.partition}:{loc.offset}")
                continue
            logger.debug(f"DETECTED: {data}")
            dm = DetectionMessage(
                frame=Frame(location=loc),
                type="detection.object",
                producer=fm.producer,
                timestamp=datetime.fromtimestamp(ts / 1000.).astimezone(),
                detections=[
                    Object.model_validate({
                        "class": k,
                        "bounding_box": {
                            "x": round(v["bounds"][0]),
                            "y": round(v["bounds"][1]),
                            "width": round(v["bounds"][2] - v["bounds"][0]),
                            "height": round(v["bounds"][3] - v["bounds"][1])
                        },
                        "confidence": round(v["percent"], 2),
                        "user_data": None,
                    })
                    for d in data for (k, v) in d.items()
                ]
            )
            logger.debug(f"DID: {dm}")
            outQ.put(copy.copy(dm))
        except Exception as e:
            logger.exception(e)
