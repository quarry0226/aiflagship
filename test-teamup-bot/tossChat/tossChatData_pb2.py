# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tossChatData.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='tossChatData.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x12tossChatData.proto\"@\n\x08\x43hatData\x12\x12\n\nteam_index\x18\x01 \x01(\x05\x12\x12\n\nroom_index\x18\x02 \x01(\x05\x12\x0c\n\x04\x63hat\x18\x03 \x01(\t\"\x1a\n\nreturnData\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\t24\n\x08tossChat\x12(\n\x0ctossChatData\x12\t.ChatData\x1a\x0b.returnData\"\x00\x62\x06proto3')
)




_CHATDATA = _descriptor.Descriptor(
  name='ChatData',
  full_name='ChatData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='team_index', full_name='ChatData.team_index', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='room_index', full_name='ChatData.room_index', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='chat', full_name='ChatData.chat', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=22,
  serialized_end=86,
)


_RETURNDATA = _descriptor.Descriptor(
  name='returnData',
  full_name='returnData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='data', full_name='returnData.data', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=88,
  serialized_end=114,
)

DESCRIPTOR.message_types_by_name['ChatData'] = _CHATDATA
DESCRIPTOR.message_types_by_name['returnData'] = _RETURNDATA
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ChatData = _reflection.GeneratedProtocolMessageType('ChatData', (_message.Message,), dict(
  DESCRIPTOR = _CHATDATA,
  __module__ = 'tossChatData_pb2'
  # @@protoc_insertion_point(class_scope:ChatData)
  ))
_sym_db.RegisterMessage(ChatData)

returnData = _reflection.GeneratedProtocolMessageType('returnData', (_message.Message,), dict(
  DESCRIPTOR = _RETURNDATA,
  __module__ = 'tossChatData_pb2'
  # @@protoc_insertion_point(class_scope:returnData)
  ))
_sym_db.RegisterMessage(returnData)



_TOSSCHAT = _descriptor.ServiceDescriptor(
  name='tossChat',
  full_name='tossChat',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=116,
  serialized_end=168,
  methods=[
  _descriptor.MethodDescriptor(
    name='tossChatData',
    full_name='tossChat.tossChatData',
    index=0,
    containing_service=None,
    input_type=_CHATDATA,
    output_type=_RETURNDATA,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_TOSSCHAT)

DESCRIPTOR.services_by_name['tossChat'] = _TOSSCHAT

# @@protoc_insertion_point(module_scope)
