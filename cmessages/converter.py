from .config import Config
from .primitives import primitives
from .types import attributes_to_fields, generate_structure


class Converter:
  """
  Conversion to and from C structures.
  """
  def __init__(self, filepaths, *args, **kwargs):
    """
    :param filepaths: List of paths to JSON files defining C structure format.
    """
    self._config = Config(filepaths)
    self._types = primitives.copy()
    self._init_type_groups()
    self._construct_types()

  def _init_type_groups(self):
    self._groups = TypeGroups()
    self._groups.sort_types(self._config.types)

  def _construct_types(self):
    process_list = self._get_initial_construction_list()
    while len(process_list):
      new_list = []
      for typename in process_list:
        if typename in self._groups.static:
          self._construct_static_type(typename)
          new_list.extend(self._config.deptree.process_type(typename))
      process_list = new_list

  def _get_initial_construction_list(self):
    process_list = list()
    for typename in primitives:
      process_list.extend(self._config.deptree.process_type(typename))
    return process_list

  def _construct_static_type(self, typename):
    typedef = self._config.types[typename]
    fields = attributes_to_fields(typedef['attributes'], self._types)
    typeclass = generate_structure(typename, fields)
    self._types[typename] = typeclass


class TypeGroups:

  def __init__(self, *args, **kwargs):
    self.static = set()
    self.other = set()

  def sort_types(self, types):
    for typename, typedef in types.items():
      self._sort_type(typename, typedef)

  def _sort_type(self, typename, typedef):
    for attr in typedef['attributes']:
      for name, type in attr.items():
        if not isinstance(type, str):
          if 'array' in type:
            self.static.add(typename)
            return
          else:
            self.other.add(typename)
            return
    self.static.add(typename)
