""" 
The setup/config script for the loggingx package.
"""

#import ez_setup
#ez_setup.use_setuptools()

from setuptools import setup, find_packages

import loggingx

setup(name=loggingx.__name__,
      version=loggingx.__version__,
      description='Extensions for the Python standard logging module.',
      author=loggingx.__author__,
      author_email=loggingx.__author_email__,
      url='http://www.ibm.com/developerworks/blog/pages/johnston',
      packages=find_packages(exclude=['test']),
      )
