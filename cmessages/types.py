from collections import Mapping, Sequence
import ctypes
from .primitives import primitives


def generate_structure(name: str, fields: list):
  """
  :param name: Name of the structure.
  :param fields: List of ctypes field definitions consisting of a tuple
                 containing the name of the field as a string and the ctypes
                 class object.
  :returns: A dynamically defined ctypes class object.
  """
  class_attr = {
    '_fields_': fields,
    '_pack_': 1,
  }
  return type(name, (ctypes.BigEndianStructure,), class_attr)

def attributes_to_fields(attributes: Mapping, types: Mapping=primitives) -> list:
  """
  :param attributes: Sequence of dictionaries containing a single key that maps
                     to a ctypes class object provided by the types parameter.
  :param types: Mapping from type names to ctypes class objects.
  """
  fields = list()
  for attr in attributes:
    for attrname, typename in attr.items():
      if isinstance(typename, str):
        ctype = types[typename]
      elif isinstance(typename, dict):
        if 'array' in typename:
          length = typename['length']
          basetype = types[typename['array']]
          ctype = basetype * length
      fields.append((attrname, ctype))
  return fields
