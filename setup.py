from setuptools import setup

# == snippet http://stackoverflow.com/questions/14399534/how-can-i-reference-requirements-txt-for-the-install-requires-kwarg-in-setuptool
from pip.req import parse_requirements

# parse_requirements() returns generator of pip.req.InstallRequirement objects
# install_reqs = parse_requirements("requirements.txt")

with open("requirements.txt", "r'") as f:
    install_reqs = f.readlines()

# reqs is a list of requirement
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
# reqs = [str(ir.req) for ir in install_reqs]

setup(name='CommanderPy',
      version='1.0',
      packages=['CommanderPy', 'CommanderPy.common',
                'CommanderPy.common.rabbit', 'CommanderPy.common.twitter',
                'CommanderPy.scripts'],
      install_requires=install_reqs,
      include_package_data=True,
      entry_points={
          'console_scripts': [
              'twitterdmchecker = CommanderPy.scripts.TwitterDMChecker:main',
          ]
      }
)
