from collections import defaultdict


class DependencyTree:
  """
  Processes C structure nesting to determine dependency.
  """

  def __init__(self, *args, **kwargs):
    self.reverse = defaultdict(set)
    self.types = dict()

  def process_config(self, cfg):
    """
    Process C structure definition configuration to determine dependency
    hierarchy.
    """
    for typename, typedef in cfg.items():
      # Determine the dependencies.
      newtype = Dependency(typedef)
      self.types[typename] = newtype
      # Store the reverse dependency map for efficient resolution.
      for deptype in newtype.dependencies:
        self.reverse[deptype].add(typename)

  def process_type(self, typename):
    """
    Mark a type as processed.
    :returns: List of types with all of their dependencies satisfied and ready
              to be processed.
    """
    resolved = list()
    parents = self.reverse[typename]
    for parentname in parents:
      parent = self.types[parentname]
      # Process the type to remove it from its set of unprocessed.
      parent.process_dependency(typename)
      # If the set is empty, return the type name to be processed.
      if not len(parent.unprocessed_dependencies):
        resolved.append(parentname)
    return resolved


class Dependency:
  """
  Description of a C structure's dependencies.
  """

  def __init__(self, cfg, *args, **kwargs):
    self.dependencies = set()
    self._load_config(cfg)

  def process_dependency(self, dep):
    if dep in self.unprocessed_dependencies:
      self.unprocessed_dependencies.remove(dep)

  def _load_config(self, cfg):
    for attr in cfg['attributes']:
      for name, type in attr.items():
        if isinstance(type, str):
          # Type strings are single members.
          self._load_member(type)
        elif isinstance(type, dict):
          # Dictionaries are arrays of members.
          self._load_member_array(type)
    self.unprocessed_dependencies = self.dependencies.copy()

  def _load_member(self, type):
    self.dependencies.add(type)

  def _load_member_array(self, type):
    if 'array' in type:
      self._load_array(type)
    elif 'variadic' in type:
      self._load_variadic_array(type)

  def _load_array(self, type):
    self.dependencies.add(type['array'])

  def _load_variadic_array(self, type):
    self.dependencies.add(type['variadic'])
