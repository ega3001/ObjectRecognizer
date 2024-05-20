from threading import Thread
import datetime as dt
import json

import confluent_kafka


class Producer:
    def __init__(self, brokers):
        conf = {'bootstrap.servers': brokers}
        self._producer = confluent_kafka.Producer(conf)
        self._cancelled = False
        self._poll_thread = Thread(target=self._poll_loop)
        self._poll_thread.start()

    def _poll_loop(self):
        while not self._cancelled:
            self._producer.poll(0.1)

    def close(self):
        self._cancelled = True
        self._poll_thread.join()

    def produce(self,
                topic: str,
                value: bytes,
                key: str = "",
                timestamp: dt.datetime = dt.datetime.utcnow(),
                on_delivery=None,
                headers: dict = {}
                ):
        self._producer.produce(
            topic=topic,
            value=value,
            key=key,
            timestamp=int(timestamp.timestamp() * 1000),
            on_delivery=on_delivery,
            headers=[(k, str(v)) for k, v in headers.items()]
        )
