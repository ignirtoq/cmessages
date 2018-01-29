from setuptools import setup, find_packages

setup(
  name='cmessages',
  version='0.0.0',
  description='Two-way translation between C structures and Python objects',
  packages=find_packages(),
  package_data={
    '': ['example.json'],
  },
)
