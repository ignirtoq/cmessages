from collections import OrderedDict
import json

from .dependencytree import DependencyTree


class Config:
  """
  Configuration file processor.
  """
  def __init__(self, filepaths, *args, **kwargs):
    self._init_configuration()
    self._load_from_files(filepaths)

  def _init_configuration(self):
    self.enum = Enum()
    self.deptree = DependencyTree()
    self.types = OrderedDict()
    self._originals = OrderedDict()

  def _load_from_files(self, filepaths):
    for filename in filepaths:
      cfg = _load_json(filename)
      self._originals[filename] = cfg.copy()
      self._load_file(cfg)

  def _load_file(self, cfg):
    if '__enum__' in cfg:
      self._load_enum(cfg.pop('__enum__'))
      self.deptree.process_config(cfg)
      self.types.update(cfg)

  def _load_enum(self, enum_cfg):
    for name, value in enum_cfg.items():
      self.enum.set(name, value)


class Enum:
  """
  Mapping between string names and numbers.
  """

  def __init__(self, *args, **kwargs):
    self.names = dict()
    self.values = dict()

  def set(self, name, value):
    self._check_name_value(name, value)
    self.names[value] = name
    self.values[name] = value

  def _check_name_value(self, name, value):
    if name in self.values and self.values[name] != value:
      raise TypeError('existing enum name does not match provided value')
    if value in self.names and self.names[value] != name:
      raise TypeError('existing enum value does not match provided name')


def _load_json(filename):
  """
  Load C structure definitions from a JSON file.
  """
  with open(filename, 'r') as filehandle:
    return _load_json_file(filehandle)

def _load_json_file(filehandle):
  return json.load(filehandle, object_pairs_hook=OrderedDict)
