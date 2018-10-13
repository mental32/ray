import re
from distutils.core import setup

def get_version():
    with open('ray/__init__.py') as inf:
      match = re.search(r"((\d\.){2,5}\d)", inf.read(), re.MULTILINE)

      if match is None:
          raise RuntimeError('Version could not be found.')
    return match.groups()[0]

setup(
    name='ray',
    version=get_version(),
    description='Fast asyncronous fortnite api library.'
)
