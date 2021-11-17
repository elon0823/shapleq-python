# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: data.proto

from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='data.proto',
  package='shapleq.proto',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\ndata.proto\x12\rshapleq.proto\"?\n\x05Group\x12\x10\n\x08group_id\x18\x01 \x01(\x04\x12\x10\n\x08owner_id\x18\x02 \x01(\x04\x12\x12\n\ngroup_name\x18\x03 \x01(\t\"1\n\tPartition\x12\x14\n\x0cpartition_id\x18\x01 \x01(\x04\x12\x0e\n\x06offset\x18\x02 \x01(\x04\"s\n\x05Topic\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\x12\x16\n\x0enum_partitions\x18\x03 \x01(\r\x12\x1a\n\x12replication_factor\x18\x04 \x01(\r\x12\x13\n\x0blast_offset\x18\x05 \x01(\x04*7\n\x0bSessionType\x12\t\n\x05\x41\x44MIN\x10\x00\x12\r\n\tPUBLISHER\x10\x01\x12\x0e\n\nSUBSCRIBER\x10\x02\x62\x06proto3'
)

_SESSIONTYPE = _descriptor.EnumDescriptor(
  name='SessionType',
  full_name='shapleq.proto.SessionType',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='ADMIN', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='PUBLISHER', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='SUBSCRIBER', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=262,
  serialized_end=317,
)
_sym_db.RegisterEnumDescriptor(_SESSIONTYPE)

SessionType = enum_type_wrapper.EnumTypeWrapper(_SESSIONTYPE)
ADMIN = 0
PUBLISHER = 1
SUBSCRIBER = 2



_GROUP = _descriptor.Descriptor(
  name='Group',
  full_name='shapleq.proto.Group',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='group_id', full_name='shapleq.proto.Group.group_id', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='owner_id', full_name='shapleq.proto.Group.owner_id', index=1,
      number=2, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='group_name', full_name='shapleq.proto.Group.group_name', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=29,
  serialized_end=92,
)


_PARTITION = _descriptor.Descriptor(
  name='Partition',
  full_name='shapleq.proto.Partition',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='partition_id', full_name='shapleq.proto.Partition.partition_id', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='offset', full_name='shapleq.proto.Partition.offset', index=1,
      number=2, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=94,
  serialized_end=143,
)


_TOPIC = _descriptor.Descriptor(
  name='Topic',
  full_name='shapleq.proto.Topic',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='shapleq.proto.Topic.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='description', full_name='shapleq.proto.Topic.description', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='num_partitions', full_name='shapleq.proto.Topic.num_partitions', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='replication_factor', full_name='shapleq.proto.Topic.replication_factor', index=3,
      number=4, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='last_offset', full_name='shapleq.proto.Topic.last_offset', index=4,
      number=5, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=145,
  serialized_end=260,
)

DESCRIPTOR.message_types_by_name['Group'] = _GROUP
DESCRIPTOR.message_types_by_name['Partition'] = _PARTITION
DESCRIPTOR.message_types_by_name['Topic'] = _TOPIC
DESCRIPTOR.enum_types_by_name['SessionType'] = _SESSIONTYPE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Group = _reflection.GeneratedProtocolMessageType('Group', (_message.Message,), {
  'DESCRIPTOR' : _GROUP,
  '__module__' : 'data_pb2'
  # @@protoc_insertion_point(class_scope:shapleq.proto.Group)
  })
_sym_db.RegisterMessage(Group)

Partition = _reflection.GeneratedProtocolMessageType('Partition', (_message.Message,), {
  'DESCRIPTOR' : _PARTITION,
  '__module__' : 'data_pb2'
  # @@protoc_insertion_point(class_scope:shapleq.proto.Partition)
  })
_sym_db.RegisterMessage(Partition)

Topic = _reflection.GeneratedProtocolMessageType('Topic', (_message.Message,), {
  'DESCRIPTOR' : _TOPIC,
  '__module__' : 'data_pb2'
  # @@protoc_insertion_point(class_scope:shapleq.proto.Topic)
  })
_sym_db.RegisterMessage(Topic)


# @@protoc_insertion_point(module_scope)
