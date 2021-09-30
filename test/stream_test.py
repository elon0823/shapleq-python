import asyncio
import logging
import threading
import time
import unittest

from kazoo.client import KazooClient

from shapleqclient.admin import Admin
from shapleqclient.base import QConfig
from shapleqclient.consumer import Consumer, FetchResult
from shapleqclient.producer import Producer
import uuid


class StreamTest(unittest.TestCase):
    zk_host = "127.0.0.1:2181"
    broker_port = 1101
    broker_address = "127.0.0.1"
    timeout = 3000
    config: QConfig
    node_id: str

    logger = logging.getLogger()
    logger.level = logging.DEBUG

    @classmethod
    def setUpClass(cls) -> None:
        cls.config = QConfig(cls.broker_address, cls.broker_port, cls.timeout)
        cls.node_id = str(uuid.uuid4()).replace('-', "", -1)

    @classmethod
    def tearDownClass(cls) -> None:
        zk = KazooClient(hosts=cls.zk_host)
        zk.start()

        zk.delete("/shapleq-debug", recursive=True)
        zk.stop()
        zk.close()

    def create_topic(self, topic: str):
        admin = Admin(self.config)
        admin.setup()
        admin.create_topic(topic, "meta", 1, 1)
        admin.close()

    def test_connect(self):
        loop = asyncio.get_event_loop()

        async def _t():
            topic = "test_topic_1"

            self.create_topic(topic)

            producer = Producer(loop, self.config, topic)
            await producer.setup()

            consumer = Consumer(loop, self.config, topic)
            await consumer.setup()

            self.assertTrue(producer.is_connected())
            self.assertTrue(consumer.is_connected())

            await consumer.terminate()
            await producer.terminate()

        loop.run_until_complete(_t())

    def test_pupsub(self):
        loop = asyncio.new_event_loop()

        async def _t():
            topic = "test_topic_2"
            expected_records = [b'google', b'paust', b'123456']
            actual_records = []

            self.create_topic(topic)

            producer = Producer(loop, self.config, topic)
            await producer.setup()

            consumer = Consumer(loop, self.config, topic)
            await consumer.setup()

            subscribe_task = loop.create_task(consumer.subscribe(0))
            wait_publish_response_task = loop.create_task(producer.wait_publish_response())

            async def on_subscribe(result: FetchResult):
                for item in result.items:
                    actual_records.append(item.data)
                if len(actual_records) == len(expected_records):
                    subscribe_task.cancel()
                    wait_publish_response_task.cancel()

            consumer.on_subscribe(on_subscribe)

            time.sleep(1)
            for seq, record in enumerate(expected_records):
                await producer.publish(record, seq, self.node_id)

            for index, data in enumerate(actual_records):
                self.assertEqual(data, expected_records[index])

            await asyncio.gather(*[subscribe_task, wait_publish_response_task])
            await producer.terminate()
            await consumer.terminate()

        loop.run_until_complete(_t())

    def test_batch_fetch(self):
        loop = asyncio.get_event_loop()

        async def _t():
            topic = "test_topic_3"
            expected_records = [b'google', b'paust', b'123456',
                                b'google2', b'paust2', b'1234562',
                                b'google3', b'paust3', b'1234563',
                                b'google4', b'paust4', b'1234564']
            actual_records = []

            self.create_topic(topic)

            producer = Producer(loop, self.config, topic)
            await producer.setup()

            consumer = Consumer(loop, self.config, topic)
            await consumer.setup()

            subscribe_task = loop.create_task(consumer.subscribe(0, max_batch_size=3, flush_interval=200))
            wait_publish_response_task = loop.create_task(producer.wait_publish_response())

            async def on_subscribe(result: FetchResult):
                for item in result.items:
                    actual_records.append(item.data)
                if len(actual_records) == len(expected_records):
                    subscribe_task.cancel()
                    wait_publish_response_task.cancel()

            consumer.on_subscribe(on_subscribe)

            time.sleep(1)
            for seq, record in enumerate(expected_records):
                await producer.publish(record, seq, self.node_id)

            for index, data in enumerate(actual_records):
                self.assertEqual(data, expected_records[index])

            await asyncio.gather(*[subscribe_task, wait_publish_response_task])
            await producer.terminate()
            await consumer.terminate()

        loop.run_until_complete(_t())