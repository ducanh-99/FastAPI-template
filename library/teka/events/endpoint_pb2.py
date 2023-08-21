# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: library/teka/events/endpoint.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import descriptor_pb2 as google_dot_protobuf_dot_descriptor__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='library/teka/events/endpoint.proto',
  package='tekone.library.teka.events',
  syntax='proto3',
  serialized_options=b'Z*go.tekoapis.com/tekone/library/teka/events',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\"library/teka/events/endpoint.proto\x12\x1atekone.library.teka.events\x1a google/protobuf/descriptor.proto*\xe7\x10\n\x08\x45ndpoint\x12$\n\x0bTEST_SOURCE\x10\x00\x1a\x13\x8a\x8e%\x0flocalhost:50052\x12$\n\x0bTEST_TARGET\x10\x01\x1a\x13\x8a\x8e%\x0flocalhost:50051\x12 \n\x1c\x44OGFOOD_HELLOWORLD_PUBLISHER\x10\x64\x12!\n\x1d\x44OGFOOD_HELLOWORLD_SUBSCRIBER\x10\x65\x12\x16\n\x12LOYALTY_SUBSCRIBER\x10\x66\x12\x12\n\x0e\x43OV_SUBSCRIBER\x10g\x12\x15\n\x11\x42ILLING_PUBLISHER\x10h\x12\x16\n\x12\x42ILLING_SUBSCRIBER\x10i\x12!\n\x1dWAREHOUSE_INVENTORY_PUBLISHER\x10j\x12\x18\n\x14\x44ISCOVERY_SUBSCRIBER\x10k\x12\x17\n\x13\x41PPROVAL_SUBSCRIBER\x10l\x12\x18\n\x13QR_SEARCH_PUBLISHER\x10\xcc\x01\x12\x17\n\x12QR_SEARCH_CONSUMER\x10\xcd\x01\x12\x16\n\x11\x42LACKLIST_SERVICE\x10\xce\x01\x12#\n\x1e\x42LACKLIST_SERVICE_PES_CONSUMER\x10\xcf\x01\x12!\n\x1c\x46OOTPRINT_PUBLISHER_CONSUMER\x10\xd0\x01\x12\x1e\n\x19\x46OOTPRINT_TRIGGER_SERVICE\x10\xd1\x01\x12\"\n\x1d\x46OOTPRINT_PUBLISHER_CONNECTOR\x10\xac\x02\x12%\n FOOTPRINT_KAFKA_MESSAGE_CONSUMER\x10\xaf\x02\x12&\n!FOOTPRINT_KAFKA_MESSAGE_PUBLISHER\x10\xb0\x02\x12\x19\n\x14\x46OOTPRINT_SUBSCRIBER\x10\xb1\x02\x12 \n\x1b\x43LEARANCE_SERVICE_PUBLISHER\x10\xb2\x02\x12\x1f\n\x1a\x43LEARANCE_SERVICE_CONSUMER\x10\xb3\x02\x12\x1f\n\x1a\x46OOTPRINT_AUDITLOG_SERVICE\x10\xb4\x02\x12 \n\x1b\x46OOTPRINT_AUDITLOG_CONSUMER\x10\xb5\x02\x12\x1a\n\x15ORDER_CAPTURE_SERVICE\x10\xb6\x02\x12\x12\n\rCONNECTOR_SBN\x10\xb7\x02\x12\x10\n\x0bPPM_SERVICE\x10\xb8\x02\x12\x17\n\x12\x43OV_NOTI_PUBLISHER\x10\xb9\x02\x12\x1d\n\x18\x45XPORT_SERVICE_PUBLISHER\x10\xba\x02\x12\x1c\n\x17\x45XPORT_SERVICE_CONSUMER\x10\xbb\x02\x12 \n\x1bWAREHOUSE_SERVICE_PUBLISHER\x10\xbc\x02\x12\x1f\n\x1aWAREHOUSE_SERVICE_CONSUMER\x10\xbd\x02\x12\x15\n\x10\x43ONNECTOR_WESCAN\x10\xbe\x02\x12 \n\x1bWAREHOUSE_CENTRAL_PUBLISHER\x10\xbf\x02\x12\x1f\n\x1aWAREHOUSE_CENTRAL_CONSUMER\x10\xc0\x02\x12\x1b\n\x16PAGE_BUILDER_PUBLISHER\x10\xc1\x02\x12#\n\x1eWAREHOUSE_ACCOUNTING_PUBLISHER\x10\xc2\x02\x12!\n\x1c\x46ULFILMENT_ROUTER_SUBSCRIBER\x10\xc3\x02\x12\x1e\n\x19\x43ONNECTOR_SOC_AND_BROTHER\x10\xc4\x02\x12\x1c\n\x17MEDUSA_SERVICE_CONSUMER\x10\xc5\x02\x12!\n\x1cSALE_REPORT_SERVICE_CONSUMER\x10\xc6\x02\x12\x1e\n\x19SUPPLIER_SERVICE_CONSUMER\x10\xc7\x02\x12$\n\x1f\x41UTOTEST_ORDER_SERVICE_CONSUMER\x10\xc8\x02\x12\x1a\n\x15\x43ONNECTOR_CP_CONSUMER\x10\xc9\x02\x12\x1e\n\x19\x43ONNECTOR_VNPOST_CONSUMER\x10\xca\x02\x12\x1b\n\x16SITE_TRANSFER_CONSUMER\x10\xcb\x02\x12\x1e\n\x19REFERRAL_SERVICE_CONSUMER\x10\xcc\x02\x12\x1f\n\x1aREFERRAL_SERVICE_PUBLISHER\x10\xcd\x02\x12\x30\n+FOOTPRINT_MERGED_CDP_PROFILE_EVENT_CONSUMER\x10\xce\x02\x12\x31\n,FOOTPRINT_MERGED_CDP_PROFILE_EVENT_PUBLISHER\x10\xcf\x02\x12\x14\n\x0f\x43\x41TALOG_SERVICE\x10\xd0\x02\x12!\n\x1c\x42LOCKCHAIN_WATCHER_PUBLISHER\x10\xd1\x02\x12 \n\x1b\x42LOCKCHAIN_WATCHER_CONSUMER\x10\xd2\x02\x12)\n$OPTIM_BOND_MARKETPLACE_BFF_PUBLISHER\x10\xd3\x02\x12(\n#OPTIM_BOND_MARKETPLACE_BFF_CONSUMER\x10\xd4\x02\x12\x1b\n\x16UNS_TRACKING_PUBLISHER\x10\xd5\x02\x12\x1a\n\x15UNS_TRACKING_CONSUMER\x10\xd6\x02\x12\'\n\"IN_HOUSE_DELIVERY_SERVICE_CONSUMER\x10\xd7\x02\x12!\n\x1cWAREHOUSE_INVENTORY_CONSUMER\x10\xd8\x02\x12!\n\x1cUNS_GROUP_MESSAGES_PUBLISHER\x10\xd9\x02\x12 \n\x1bUNS_GROUP_MESSAGES_CONSUMER\x10\xda\x02\x12&\n!FOOTPRINT_TRACKING_EVENT_CONSUMER\x10\xdb\x02\x12\'\n\"FOOTPRINT_TRACKING_EVENT_PUBLISHER\x10\xdc\x02\x12#\n\x1eWAREHOUSE_AGGREGATOR_PUBLISHER\x10\xdd\x02\x12\"\n\x1dWAREHOUSE_AGGREGATOR_CONSUMER\x10\xde\x02:4\n\x07\x61\x64\x64ress\x12!.google.protobuf.EnumValueOptions\x18\xe1\xd1\x04 \x01(\tB,Z*go.tekoapis.com/tekone/library/teka/eventsb\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_descriptor__pb2.DESCRIPTOR,])

_ENDPOINT = _descriptor.EnumDescriptor(
  name='Endpoint',
  full_name='tekone.library.teka.events.Endpoint',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='TEST_SOURCE', index=0, number=0,
      serialized_options=b'\212\216%\017localhost:50052',
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='TEST_TARGET', index=1, number=1,
      serialized_options=b'\212\216%\017localhost:50051',
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DOGFOOD_HELLOWORLD_PUBLISHER', index=2, number=100,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DOGFOOD_HELLOWORLD_SUBSCRIBER', index=3, number=101,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='LOYALTY_SUBSCRIBER', index=4, number=102,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='COV_SUBSCRIBER', index=5, number=103,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='BILLING_PUBLISHER', index=6, number=104,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='BILLING_SUBSCRIBER', index=7, number=105,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='WAREHOUSE_INVENTORY_PUBLISHER', index=8, number=106,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DISCOVERY_SUBSCRIBER', index=9, number=107,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='APPROVAL_SUBSCRIBER', index=10, number=108,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='QR_SEARCH_PUBLISHER', index=11, number=204,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='QR_SEARCH_CONSUMER', index=12, number=205,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='BLACKLIST_SERVICE', index=13, number=206,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='BLACKLIST_SERVICE_PES_CONSUMER', index=14, number=207,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='FOOTPRINT_PUBLISHER_CONSUMER', index=15, number=208,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='FOOTPRINT_TRIGGER_SERVICE', index=16, number=209,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='FOOTPRINT_PUBLISHER_CONNECTOR', index=17, number=300,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='FOOTPRINT_KAFKA_MESSAGE_CONSUMER', index=18, number=303,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='FOOTPRINT_KAFKA_MESSAGE_PUBLISHER', index=19, number=304,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='FOOTPRINT_SUBSCRIBER', index=20, number=305,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CLEARANCE_SERVICE_PUBLISHER', index=21, number=306,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CLEARANCE_SERVICE_CONSUMER', index=22, number=307,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='FOOTPRINT_AUDITLOG_SERVICE', index=23, number=308,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='FOOTPRINT_AUDITLOG_CONSUMER', index=24, number=309,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ORDER_CAPTURE_SERVICE', index=25, number=310,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CONNECTOR_SBN', index=26, number=311,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='PPM_SERVICE', index=27, number=312,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='COV_NOTI_PUBLISHER', index=28, number=313,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='EXPORT_SERVICE_PUBLISHER', index=29, number=314,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='EXPORT_SERVICE_CONSUMER', index=30, number=315,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='WAREHOUSE_SERVICE_PUBLISHER', index=31, number=316,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='WAREHOUSE_SERVICE_CONSUMER', index=32, number=317,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CONNECTOR_WESCAN', index=33, number=318,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='WAREHOUSE_CENTRAL_PUBLISHER', index=34, number=319,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='WAREHOUSE_CENTRAL_CONSUMER', index=35, number=320,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='PAGE_BUILDER_PUBLISHER', index=36, number=321,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='WAREHOUSE_ACCOUNTING_PUBLISHER', index=37, number=322,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='FULFILMENT_ROUTER_SUBSCRIBER', index=38, number=323,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CONNECTOR_SOC_AND_BROTHER', index=39, number=324,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='MEDUSA_SERVICE_CONSUMER', index=40, number=325,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='SALE_REPORT_SERVICE_CONSUMER', index=41, number=326,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='SUPPLIER_SERVICE_CONSUMER', index=42, number=327,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='AUTOTEST_ORDER_SERVICE_CONSUMER', index=43, number=328,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CONNECTOR_CP_CONSUMER', index=44, number=329,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CONNECTOR_VNPOST_CONSUMER', index=45, number=330,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='SITE_TRANSFER_CONSUMER', index=46, number=331,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='REFERRAL_SERVICE_CONSUMER', index=47, number=332,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='REFERRAL_SERVICE_PUBLISHER', index=48, number=333,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='FOOTPRINT_MERGED_CDP_PROFILE_EVENT_CONSUMER', index=49, number=334,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='FOOTPRINT_MERGED_CDP_PROFILE_EVENT_PUBLISHER', index=50, number=335,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CATALOG_SERVICE', index=51, number=336,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='BLOCKCHAIN_WATCHER_PUBLISHER', index=52, number=337,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='BLOCKCHAIN_WATCHER_CONSUMER', index=53, number=338,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='OPTIM_BOND_MARKETPLACE_BFF_PUBLISHER', index=54, number=339,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='OPTIM_BOND_MARKETPLACE_BFF_CONSUMER', index=55, number=340,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='UNS_TRACKING_PUBLISHER', index=56, number=341,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='UNS_TRACKING_CONSUMER', index=57, number=342,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='IN_HOUSE_DELIVERY_SERVICE_CONSUMER', index=58, number=343,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='WAREHOUSE_INVENTORY_CONSUMER', index=59, number=344,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='UNS_GROUP_MESSAGES_PUBLISHER', index=60, number=345,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='UNS_GROUP_MESSAGES_CONSUMER', index=61, number=346,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='FOOTPRINT_TRACKING_EVENT_CONSUMER', index=62, number=347,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='FOOTPRINT_TRACKING_EVENT_PUBLISHER', index=63, number=348,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='WAREHOUSE_AGGREGATOR_PUBLISHER', index=64, number=349,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='WAREHOUSE_AGGREGATOR_CONSUMER', index=65, number=350,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=101,
  serialized_end=2252,
)
_sym_db.RegisterEnumDescriptor(_ENDPOINT)

Endpoint = enum_type_wrapper.EnumTypeWrapper(_ENDPOINT)
TEST_SOURCE = 0
TEST_TARGET = 1
DOGFOOD_HELLOWORLD_PUBLISHER = 100
DOGFOOD_HELLOWORLD_SUBSCRIBER = 101
LOYALTY_SUBSCRIBER = 102
COV_SUBSCRIBER = 103
BILLING_PUBLISHER = 104
BILLING_SUBSCRIBER = 105
WAREHOUSE_INVENTORY_PUBLISHER = 106
DISCOVERY_SUBSCRIBER = 107
APPROVAL_SUBSCRIBER = 108
QR_SEARCH_PUBLISHER = 204
QR_SEARCH_CONSUMER = 205
BLACKLIST_SERVICE = 206
BLACKLIST_SERVICE_PES_CONSUMER = 207
FOOTPRINT_PUBLISHER_CONSUMER = 208
FOOTPRINT_TRIGGER_SERVICE = 209
FOOTPRINT_PUBLISHER_CONNECTOR = 300
FOOTPRINT_KAFKA_MESSAGE_CONSUMER = 303
FOOTPRINT_KAFKA_MESSAGE_PUBLISHER = 304
FOOTPRINT_SUBSCRIBER = 305
CLEARANCE_SERVICE_PUBLISHER = 306
CLEARANCE_SERVICE_CONSUMER = 307
FOOTPRINT_AUDITLOG_SERVICE = 308
FOOTPRINT_AUDITLOG_CONSUMER = 309
ORDER_CAPTURE_SERVICE = 310
CONNECTOR_SBN = 311
PPM_SERVICE = 312
COV_NOTI_PUBLISHER = 313
EXPORT_SERVICE_PUBLISHER = 314
EXPORT_SERVICE_CONSUMER = 315
WAREHOUSE_SERVICE_PUBLISHER = 316
WAREHOUSE_SERVICE_CONSUMER = 317
CONNECTOR_WESCAN = 318
WAREHOUSE_CENTRAL_PUBLISHER = 319
WAREHOUSE_CENTRAL_CONSUMER = 320
PAGE_BUILDER_PUBLISHER = 321
WAREHOUSE_ACCOUNTING_PUBLISHER = 322
FULFILMENT_ROUTER_SUBSCRIBER = 323
CONNECTOR_SOC_AND_BROTHER = 324
MEDUSA_SERVICE_CONSUMER = 325
SALE_REPORT_SERVICE_CONSUMER = 326
SUPPLIER_SERVICE_CONSUMER = 327
AUTOTEST_ORDER_SERVICE_CONSUMER = 328
CONNECTOR_CP_CONSUMER = 329
CONNECTOR_VNPOST_CONSUMER = 330
SITE_TRANSFER_CONSUMER = 331
REFERRAL_SERVICE_CONSUMER = 332
REFERRAL_SERVICE_PUBLISHER = 333
FOOTPRINT_MERGED_CDP_PROFILE_EVENT_CONSUMER = 334
FOOTPRINT_MERGED_CDP_PROFILE_EVENT_PUBLISHER = 335
CATALOG_SERVICE = 336
BLOCKCHAIN_WATCHER_PUBLISHER = 337
BLOCKCHAIN_WATCHER_CONSUMER = 338
OPTIM_BOND_MARKETPLACE_BFF_PUBLISHER = 339
OPTIM_BOND_MARKETPLACE_BFF_CONSUMER = 340
UNS_TRACKING_PUBLISHER = 341
UNS_TRACKING_CONSUMER = 342
IN_HOUSE_DELIVERY_SERVICE_CONSUMER = 343
WAREHOUSE_INVENTORY_CONSUMER = 344
UNS_GROUP_MESSAGES_PUBLISHER = 345
UNS_GROUP_MESSAGES_CONSUMER = 346
FOOTPRINT_TRACKING_EVENT_CONSUMER = 347
FOOTPRINT_TRACKING_EVENT_PUBLISHER = 348
WAREHOUSE_AGGREGATOR_PUBLISHER = 349
WAREHOUSE_AGGREGATOR_CONSUMER = 350

ADDRESS_FIELD_NUMBER = 76001
address = _descriptor.FieldDescriptor(
  name='address', full_name='tekone.library.teka.events.address', index=0,
  number=76001, type=9, cpp_type=9, label=1,
  has_default_value=False, default_value=b"".decode('utf-8'),
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key)

DESCRIPTOR.enum_types_by_name['Endpoint'] = _ENDPOINT
DESCRIPTOR.extensions_by_name['address'] = address
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

google_dot_protobuf_dot_descriptor__pb2.EnumValueOptions.RegisterExtension(address)

DESCRIPTOR._options = None
_ENDPOINT.values_by_name["TEST_SOURCE"]._options = None
_ENDPOINT.values_by_name["TEST_TARGET"]._options = None
# @@protoc_insertion_point(module_scope)
