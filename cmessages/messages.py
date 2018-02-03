from collections import OrderedDict


class Message(OrderedDict):

  def __init__(self, *args, **kwargs):
    if len(args):
      self.type = args[0]
      args = args[1:]
    elif 'type' in kwargs:
      self.type = kwargs.pop('type')
    super().__init__(*args, **kwargs)
