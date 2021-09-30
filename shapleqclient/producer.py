import threading
from shapleqclient.base import ClientBase, QConfig
from shapleqclient.common.exception import InvalidMessageError, SocketClosedError, RequestFailedError, InvalidNodeIdError
from shapleqclient.proto.api_pb2 import PutResponse, Ack
from shapleqclient.proto.data_pb2 import SessionType
from shapleqclient.message.qmessage import QMessage, MessageType, make_qmessage_from_proto
from shapleqclient.message.api import put_msg
import asyncio


class Producer(ClientBase):
    topic: str

    def __init__(self, loop: asyncio.AbstractEventLoop, config: QConfig, topic: str):
        super().__init__(loop, "ShapleQ-Producer", config)
        self.topic = topic

    async def setup(self):
        await self.connect(SessionType.PUBLISHER, self.topic)

    async def terminate(self):
        await self.close()

    async def publish(self, data: bytes, seq_num: int, node_id: str):
        if not self.is_connected():
            raise SocketClosedError()
        if len(node_id) != 32:
            raise InvalidNodeIdError()
        msg = make_qmessage_from_proto(MessageType.STREAM, put_msg(data, seq_num, node_id))
        await self._send_message(msg)

    async def wait_publish_response(self):
        try:
            async for received in self.continuous_receive():
                self._handle_message(received)
        except (SocketClosedError, asyncio.CancelledError):
            return

    def _handle_message(self, msg: QMessage):

        if (put_response := msg.unpack_to(PutResponse())) is not None:
            self.logger.debug('received response - partition id: {}, partition offset: {}'.format(
                put_response.partition.partition_id, put_response.partition.offset))
        elif (ack := msg.unpack_to(Ack())) is not None:
            raise RequestFailedError(msg=ack.msg)
        else:
            raise InvalidMessageError()
