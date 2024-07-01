from setuptools import setup, find_packages

from own import __version__
from version import get_and_increment

setup(name="Find & Copy PDF files",
      python_requires=">=3.12",
      version=f'{__version__}.dev{get_and_increment()}',
      packages = find_packages(include=["own"]),
      entry_points =
        {'console_scripts': ['Find & Copy PDF files=own.__main__:gui']
        })
