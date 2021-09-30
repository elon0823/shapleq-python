from shapleqclient.base import QConfig
from shapleqclient.message.qmessage import MessageType, make_qmessage_from_proto, make_qmessage_from_buffer, QMessage
from shapleqclient.message.api import create_topic_msg, delete_topic_msg, describe_topic_msg, list_topic_msg, ping_msg
from shapleqclient.proto.api_pb2 import CreateTopicResponse, DeleteTopicResponse, ListTopicResponse, DescribeTopicResponse, Pong
from shapleqclient.proto.data_pb2 import Topic
from shapleqclient.common.exception import MessageDecodeError, RequestFailedError, ClientConnectionError, \
    SocketWriteError, SocketClosedError, NotEnoughBufferError, SocketReadError
from shapleqclient.common.error import PQErrCode
from typing import List
import logging
import socket


class Admin:
    connected: bool = False
    config: QConfig
    logger: logging.Logger
    _sock: socket.socket

    def __init__(self, config: QConfig):
        self.logger = logging.getLogger("ShapleQ-AdminClient")
        self.config = config

    def _connect(self, address: str, port: int):
        if self.connected:
            raise ClientConnectionError("already connected to broker")

        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.settimeout(self.config.get_timeout() / 1000)
        try:
            self._sock.connect((address, port))
            self.connected = True
            self.logger.info('connected to broker target {}:{}'.format(address, port))

        except socket.timeout:
            raise ClientConnectionError("cannot connect to broker : timeout")

    def _send_message(self, msg: QMessage):
        if self._sock.send(msg.serialize()) <= 0:
            raise SocketWriteError()
        self.logger.info('sent data successfully')

    def _read_message(self) -> QMessage:
        while True:
            if not self.connected:
                raise SocketClosedError()

            try:
                received = self._sock.recv(4 * 1024)
                if not received:
                    self.close()
                    raise SocketClosedError()
                self.logger.info('read data successfully')

                return make_qmessage_from_buffer(received)
            except NotEnoughBufferError:
                continue
            except socket.error as msg:
                self.logger.error(msg)
                self.close()
                raise SocketReadError()

    def setup(self):
        self._connect(self.config.get_broker_address(), self.config.get_broker_port())

    def close(self):
        if self.connected:
            self.connected = False
            self._sock.close()
            self.logger.info('connection closed')

    def create_topic(self, topic_name: str, topic_meta: str, num_partitions: int, replication_factor: int):
        msg = make_qmessage_from_proto(MessageType.TRANSACTION,
                                       create_topic_msg(topic_name, topic_meta, num_partitions, replication_factor))
        self._send_message(msg)
        received = self._read_message()

        response = CreateTopicResponse()
        if received.unpack_to(response) is None:
            raise MessageDecodeError(msg="cannot unpack to `CreateTopicResponse`")

        if response.error_code != PQErrCode.Success.value:
            self.logger.error(response.error_message)
            raise RequestFailedError(msg=response.error_message)

    def delete_topic(self, topic_name: str):
        msg = make_qmessage_from_proto(MessageType.TRANSACTION, delete_topic_msg(topic_name))
        self._send_message(msg)
        received = self._read_message()

        response = DeleteTopicResponse()
        if received.unpack_to(response) is None:
            raise MessageDecodeError(msg="cannot unpack to `DeleteTopicResponse`")

        if response.error_code != PQErrCode.Success.value:
            self.logger.error(response.error_message)
            raise RequestFailedError(msg=response.error_message)

    def describe_topic(self, topic_name: str) -> Topic:
        msg = make_qmessage_from_proto(MessageType.TRANSACTION, describe_topic_msg(topic_name))
        self._send_message(msg)
        received = self._read_message()

        response = DescribeTopicResponse()
        if received.unpack_to(response) is None:
            raise MessageDecodeError(msg="cannot unpack to `DescribeTopicResponse`")

        if response.error_code != PQErrCode.Success.value:
            self.logger.error(response.error_message)
            raise RequestFailedError(msg=response.error_message)

        return response.topic

    def list_topic(self) -> List[Topic]:
        msg = make_qmessage_from_proto(MessageType.TRANSACTION, list_topic_msg())
        self._send_message(msg)
        received = self._read_message()

        response = ListTopicResponse()
        if received.unpack_to(response) is None:
            raise MessageDecodeError(msg="cannot unpack to `ListTopicResponse`")

        if response.error_code != PQErrCode.Success.value:
            self.logger.error(response.error_message)
            raise RequestFailedError(msg=response.error_message)

        return response.topics

    def heartbeat(self, msg: str, broker_id: int) -> Pong:
        msg = make_qmessage_from_proto(MessageType.TRANSACTION, ping_msg(msg, broker_id))
        self._send_message(msg)
        received = self._read_message()

        response = Pong()
        if received.unpack_to(response) is None:
            raise MessageDecodeError(msg="cannot unpack to `Pong`")

        return response
