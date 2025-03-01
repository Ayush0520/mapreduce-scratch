# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: MapReduce.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0fMapReduce.proto\x12\x06kmeans\"\x88\x01\n\x10MapperParameters\x12\x11\n\tmapper_id\x18\x01 \x01(\t\x12\x13\n\x0bstart_index\x18\x02 \x01(\x05\x12\x11\n\tend_index\x18\x03 \x01(\x05\x12#\n\tcentroids\x18\x04 \x03(\x0b\x32\x10.kmeans.Centroid\x12\x14\n\x0cnum_reducers\x18\x05 \x01(\x05\",\n\x08\x43\x65ntroid\x12\n\n\x02id\x18\x01 \x01(\t\x12\t\n\x01x\x18\x02 \x01(\x02\x12\t\n\x01y\x18\x03 \x01(\x02\" \n\x0eMapperResponse\x12\x0e\n\x06status\x18\x01 \x01(\t\"=\n\x11ReducerParameters\x12\x14\n\x0c\x64\x61ta_request\x18\x01 \x01(\t\x12\x12\n\nreducer_id\x18\x02 \x01(\t\"9\n\x0fReducerResponse\x12&\n\x0b\x64\x61ta_points\x18\x01 \x03(\x0b\x32\x11.kmeans.DataPoint\"6\n\tDataPoint\x12\x13\n\x0b\x63\x65ntroid_id\x18\x01 \x01(\t\x12\t\n\x01x\x18\x02 \x01(\t\x12\t\n\x01y\x18\x03 \x01(\t\">\n\x10InvokeParameters\x12\x13\n\x0bnum_mappers\x18\x01 \x01(\x05\x12\x15\n\rnum_centroids\x18\x02 \x01(\x05\"}\n\x0eInvokeResponse\x12.\n\x04\x64\x61ta\x18\x01 \x03(\x0b\x32 .kmeans.InvokeResponse.DataEntry\x1a;\n\tDataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x1d\n\x05value\x18\x02 \x01(\x0b\x32\x0e.kmeans.Points:\x02\x38\x01\"\x1d\n\x05Point\x12\t\n\x01x\x18\x01 \x01(\t\x12\t\n\x01y\x18\x02 \x01(\t\"\'\n\x06Points\x12\x1d\n\x06points\x18\x01 \x03(\x0b\x32\r.kmeans.Point2\x9c\x01\n\rMapperService\x12?\n\x0bperform_map\x12\x18.kmeans.MapperParameters\x1a\x16.kmeans.MapperResponse\x12J\n\x14send_data_to_reducer\x12\x19.kmeans.ReducerParameters\x1a\x17.kmeans.ReducerResponse2T\n\x0eReducerService\x12\x42\n\x0einvoke_reducer\x12\x18.kmeans.InvokeParameters\x1a\x16.kmeans.InvokeResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'MapReduce_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_INVOKERESPONSE_DATAENTRY']._options = None
  _globals['_INVOKERESPONSE_DATAENTRY']._serialized_options = b'8\001'
  _globals['_MAPPERPARAMETERS']._serialized_start=28
  _globals['_MAPPERPARAMETERS']._serialized_end=164
  _globals['_CENTROID']._serialized_start=166
  _globals['_CENTROID']._serialized_end=210
  _globals['_MAPPERRESPONSE']._serialized_start=212
  _globals['_MAPPERRESPONSE']._serialized_end=244
  _globals['_REDUCERPARAMETERS']._serialized_start=246
  _globals['_REDUCERPARAMETERS']._serialized_end=307
  _globals['_REDUCERRESPONSE']._serialized_start=309
  _globals['_REDUCERRESPONSE']._serialized_end=366
  _globals['_DATAPOINT']._serialized_start=368
  _globals['_DATAPOINT']._serialized_end=422
  _globals['_INVOKEPARAMETERS']._serialized_start=424
  _globals['_INVOKEPARAMETERS']._serialized_end=486
  _globals['_INVOKERESPONSE']._serialized_start=488
  _globals['_INVOKERESPONSE']._serialized_end=613
  _globals['_INVOKERESPONSE_DATAENTRY']._serialized_start=554
  _globals['_INVOKERESPONSE_DATAENTRY']._serialized_end=613
  _globals['_POINT']._serialized_start=615
  _globals['_POINT']._serialized_end=644
  _globals['_POINTS']._serialized_start=646
  _globals['_POINTS']._serialized_end=685
  _globals['_MAPPERSERVICE']._serialized_start=688
  _globals['_MAPPERSERVICE']._serialized_end=844
  _globals['_REDUCERSERVICE']._serialized_start=846
  _globals['_REDUCERSERVICE']._serialized_end=930
# @@protoc_insertion_point(module_scope)
