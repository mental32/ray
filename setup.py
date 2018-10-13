from distutils.core import setup

with open('ray/__init__.py') as inf:
    for line in inf:
        if line.startswith('__version__ = '):
            version = line.strip('_version =\'')

setup(
    name='ray',
    version=version,
    description='Fast asyncronous fortnite api library.'
)
