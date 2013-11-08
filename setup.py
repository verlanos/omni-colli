#!/usr/bin/env python
__author__ = 'Sefverl'

from distutils.core import setup

setup(name="OmniColli",
      version="0.1",
      description="Raw data collection framework",
      author="Sefverl Balasingam",
      author_email="svxarda@hotmail.com",
      url="https://github.com/verlanos/omni-colli",
      packages=["client", "server", "crypto", "tests"]
)


