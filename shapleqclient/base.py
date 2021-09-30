import socket
from shapleqclient.proto.data_pb2 import SessionType
from shapleqclient.proto.api_pb2 import DiscoverBrokerResponse, ConnectResponse, Ack
from shapleqclient.common.exception import *
from shapleqclient.message.qmessage import *
from shapleqclient.message.api import discover_broker_msg, connect_msg
from shapleqclient.common.error import PQErrCode
from typing import Generator
import logging
import asyncio


class QConfig:
    DEFAULT_TIMEOUT = 3000
    DEFAULT_BROKER_HOST = "localhost"
    DEFAULT_BROKER_PORT = 1101

    # timeout should be milliseconds value
    def __init__(self, broker_address: str = DEFAULT_BROKER_HOST, broker_port: int = DEFAULT_BROKER_PORT,
                 timeout: int = DEFAULT_TIMEOUT):
        self.broker_address = broker_address
        self.broker_port = broker_port
        self.timeout = timeout

    def get_broker_address(self) -> str:
        return self.broker_address

    def get_broker_port(self) -> int:
        return self.broker_port

    def get_timeout(self) -> int:
        return self.timeout


class ClientBase:
    connected: bool = False
    config: QConfig
    logger: logging.Logger
    _sock: socket.socket
    _loop: asyncio.AbstractEventLoop
    _reader: asyncio.StreamReader
    _writer: asyncio.StreamWriter

    def __init__(self, loop: asyncio.AbstractEventLoop, name: str, config: QConfig):
        self._loop = loop
        self.logger = logging.getLogger(name)
        self.config = config

    def is_connected(self) -> bool:
        return self.connected

    async def _connect_to_broker(self, address: str, port: int):
        if self.connected:
            raise ClientConnectionError("already connected to broker")
        asyncio.set_event_loop(self._loop)
        try:
            future = asyncio.open_connection(address, port)
            self._reader, self._writer = await asyncio.wait_for(future, timeout=self.config.get_timeout())
            self.connected = True
            self.logger.info('connected to broker target {}:{}'.format(address, port))

        except (asyncio.TimeoutError, ConnectionError, OSError) as e:
            raise ClientConnectionError("cannot connect to broker : {}".format(e))

    async def _send_message(self, msg: QMessage):
        self._writer.write(msg.serialize())
        try:
            await asyncio.wait_for(self._writer.drain(), timeout=self.config.get_timeout())
        except (asyncio.TimeoutError, ConnectionError, OSError) as e:
            raise SocketWriteError(str(e))
        self.logger.info('sent data successfully')

    async def _read_message(self) -> QMessage:
        msg_buf: bytearray = bytearray()
        while True:
            if not self.is_connected():
                raise SocketClosedError()

            try:
                received = await self._reader.read(4 * 1024)
                if not received:
                    await self.close()
                    raise SocketClosedError()
                self.logger.info('read data successfully')
                msg_buf += bytearray(received)

                return make_qmessage_from_buffer(received)
            except NotEnoughBufferError:
                continue
            except (ConnectionError, TimeoutError, OSError) as e:
                self.logger.error(e)
                await self.close()
                raise SocketReadError(str(e))

    async def continuous_receive(self) -> Generator[QMessage, None, None]:
        msg_buf: bytearray = bytearray()

        while True:
            if not self.is_connected():
                raise SocketClosedError()

            try:
                received = await self._reader.read(4 * 1024)
                if not received:
                    await self.close()
                    raise SocketClosedError()
            except asyncio.TimeoutError:
                continue
            except (ConnectionError, OSError) as e:
                self.logger.error(e)
                await self.close()
                raise SocketReadError()

            self.logger.info('received data')
            msg_buf += bytearray(received)

            # unmarshal QMessages from received buffer
            while True:
                try:
                    qmsg = make_qmessage_from_buffer(msg_buf)
                    yield qmsg

                    read_bytes = QHeader.HEADER_SIZE + qmsg.length()
                    msg_buf = msg_buf[read_bytes:]

                except NotEnoughBufferError:
                    break
            await asyncio.sleep(0)

    async def _init_stream(self, session_type: SessionType, topic: str):
        if not self.is_connected():
            raise SocketClosedError()

        msg = make_qmessage_from_proto(MessageType.STREAM, connect_msg(session_type, topic))
        await self._send_message(msg)
        received = await self._read_message()

        if received.unpack_to(ConnectResponse()) is not None:
            self.logger.info('stream initialized')
            return
        elif (ack := msg.unpack_to(Ack())) is not None:
            raise RequestFailedError(msg=ack.msg)
        else:
            raise InvalidMessageError()

    async def connect(self, session_type: SessionType, topic: str):
        if len(topic) == 0:
            raise TopicNotSetError()

        await self._connect_to_broker(self.config.get_broker_address(), self.config.get_broker_port())
        msg = make_qmessage_from_proto(MessageType.TRANSACTION, discover_broker_msg(topic, session_type))

        await self._send_message(msg)
        received = await self._read_message()

        discover_broker_response = DiscoverBrokerResponse()
        if received.unpack_to(discover_broker_response) is None:
            raise MessageDecodeError(msg="cannot unpack to `DiscoverBrokerResponse`")

        if discover_broker_response.error_code != PQErrCode.Success.value:
            raise RequestFailedError(msg=discover_broker_response.error_message)

        await self.close()
        new_addr = discover_broker_response.address.split(':')
        await self._connect_to_broker(new_addr[0], int(new_addr[1]))
        await self._init_stream(session_type, topic)

    async def close(self):
        if self.connected:
            self.connected = False
            self._writer.close()
            await self._writer.wait_closed()
            self.logger.info('connection closed')
