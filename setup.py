from distutils.core import setup

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pygw2tools',
    version='',
    packages=['gw2db', 'gw2db.auths', 'gw2db.items', 'gw2db.miscs', 'gw2db.profs', 'gw2db.story'],
    url='https://github.com/zanar/pygw2tools',
    license='GPLv3',
    author='bzed',
    author_email='zanar.dev@protonmail.com',
    description='Set of off-game tools for Guild Wars 2',
    install_requires=['sqlalchemy', 'requests', 'tzlocal'],
)
