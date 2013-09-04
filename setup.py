#!/usr/bin/env python
from distutils.core import setup

setup(name = "shift_planning",
    version = "110",
    description = "Shiftplanning API for Python",
    author = "shiftplanning.com",
    author_email = "support@shiftplanning.com",
    url = "http://shiftplanning.com/api",
    packages = ['shift_planning'],
    package_data = {'shift_planning' : ['__init__.py'] },
    requires = ['simplejson']
) 
