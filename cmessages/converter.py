from .config import Config
from .primitives import primitives
from .types import attributes_to_fields, generate_structure, DefaultHeader


class Converter:
  """
  Conversion to and from C structures.
  """
  def __init__(self, filepaths, header=(DefaultHeader,'type'),
               *args, **kwargs):
    """
    :param filepaths: List of paths to JSON files defining C structure format.
    :param header: Tuple defining the message header.  The first element must
                   be a class derived from ctypes.BigEndianStructure.  The
                   second element is the string name of the header member
                   denoting the structure type enum value.
    """
    self._config = Config(filepaths)
    self._set_header(header)
    self._types = primitives.copy()
    self._init_type_groups()
    self._construct_types()

  # Public API

  def get_enum(self, bytestring):
    if self._header_class is None:
      raise TypeError('No header defined; cannot get enum from bytestring')
    hdr = self._header_class.from_buffer_copy(bytestring, offset=0)
    return getattr(hdr, self._header_type_member)

  def to_bytes(self, data):
    pass

  def to_dict(self, bytestring):
    pass

  def to_object(self, bytestring):
    pass

  # Private methods

  def _set_header(self, header):
    if header is not None:
      self._header_class = header[0]
      self._header_type_member = header[1]
    else:
      self._header_class = None
      self._header_type = None

  def _init_type_groups(self):
    self._groups = TypeGroups()
    self._groups.sort_types(self._config.types)

  def _construct_types(self):
    deptree = self._config.deptree
    # Reset the tree to make sure we can traverse it.
    deptree.reset()
    process_list = _get_initial_construction_list(deptree)
    while len(process_list):
      new_list = []
      for typename in process_list:
        if typename in self._groups.static:
          self._construct_static_type(typename)
          new_list.extend(deptree.process_type(typename))
      process_list = new_list

  def _construct_static_type(self, typename):
    """
    Create a ctypes class object from a statically-sized, possibly nested
    C structure definition.
    """
    typedef = self._config.types[typename]
    fields = attributes_to_fields(typedef['attributes'], self._types)
    typeclass = generate_structure(typename, fields)
    self._types[typename] = typeclass


class TypeGroups:
  """
  Sort types into groups based on size category.
  """
  def __init__(self, *args, **kwargs):
    self.static = set()
    self.variadic = set()

  def sort_types(self, types, deptree):
    """
    Sort structures into statically sized and variadic.
    """
    # Reset the tree to make sure we can traverse it.
    deptree.reset()
    process_list = _get_initial_construction_list(deptree)
    while len(process_list):
      new_list[]
      for typename in process_list:
        typedef = types[typename]
        self._sort_type(typename, typedef)
        new_list.extend(deptree.process_type(typename))
      process_list = new_list

  def _sort_type(self, typename, typedef):
    for attr in typedef['attributes']:
      for type in attr.values():
        if isinstance(type, str):
          if type in self.variadic:
            self.variadic.add(typename)
            return
        else:
          if 'variadic' in type:
            self.variadic.add(typename)
            return
    self.static.add(typename)


def _get_initial_construction_list(deptree):
  process_list = list()
  for typename in primitives:
    process_list.extend(deptree.process_type(typename))
  return process_list
