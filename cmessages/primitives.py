"""
Mapping of standard C type names to their ctypes class.
"""
import ctypes

#
primitives = {
# Standard types.
  'char': ctypes.c_int8,
  'byte': ctypes.c_int8,
  'unsigned char': ctypes.c_uint8,
  'unsigned byte': ctypes.c_uint8,
  'short': ctypes.c_int16,
  'unsigned short': ctypes.c_uint16,
  'int': ctypes.c_int32,
  'unsigned int': ctypes.c_uint32,
  'unsigned': ctypes.c_uint32,
  'long': ctypes.c_int32,
  'unsigned long': ctypes.c_uint32,
  'long long': ctypes.c_int64,
  'unsigned long long': ctypes.c_uint64,
# Fixed-width types.
  'int8_t': ctypes.c_int8,
  'uint8_t': ctypes.c_uint8,
  'int16_t': ctypes.c_int16,
  'uint16_t': ctypes.c_uint16,
  'int32_t': ctypes.c_int32,
  'uint32_t': ctypes.c_uint32,
  'int64_t': ctypes.c_int64,
  'uint64_t': ctypes.c_uint64,
}
