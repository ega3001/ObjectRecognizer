from contextlib import closing

import confluent_kafka


class Consumer:
    def __init__(self, brokers: str, group: str):
        self._consumer = confluent_kafka.Consumer({
            'bootstrap.servers': brokers,
            'group.id': group,
            'session.timeout.ms': 6000,
            'auto.offset.reset': 'largest',
            'enable.auto.offset.store': False,
            'enable.auto.commit': False
        })

    def consume(self, topics: list):
        self._consumer.subscribe(topics)
        # self._consumer.assign(
        #     [confluent_kafka.TopicPartition(topic, 0) for topic in topics])
        with closing(self._consumer) as c:
            while True:
                msg = c.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    raise confluent_kafka.KafkaException(msg.error())
                else:
                    yield msg
                # c.store_offsets(msg)
