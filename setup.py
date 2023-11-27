#!/usr/bin/env python3
import os
import re
import sys
import datetime
import subprocess
from Crypto.Cipher import AES
from binascii import a2b_hex
import uuid
import socket
import encry
## License check


import Cython
import disutils
import os
from distutils.core import setup
from Cython.Build import cythonize
py_files = ['states.py',]
setup(ext_modules = cythonize(py_files),)

# # gen_license_file()
# encry.license_check()
