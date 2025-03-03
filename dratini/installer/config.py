#---------#
# Imports #
#---------#

import os
from dratini.platform import *

#---------#
# Project #
#---------#

from dratini.projectconfig import *

#---------------#
# Logging Tools #
#---------------#

ECHO = "echo"

#---------------#
# Install Tools #
#---------------#

CHMOD = "chmod"
CP = "cp"
LN = "ln"
RM = "rm"
SUDO = "sudo"

#-----------#
# Technical #
#-----------#

# The root directory to use when installing and uninstalling.
ROOT = "/usr/local"

if is_windows():
    ROOT = "C:\\Program Files\\dratini"

# The path to the main executable.
BIN_PATH = PROJECT.name + ".py"

# The directory to install binaries to.
INSTALL_BIN_DIR = os.path.join(ROOT, "bin")

if is_windows():
    INSTALL_BIN_DIR = ROOT

# The directory to install libraries to.
INSTALL_LIB_DIR = os.path.join(ROOT, "lib")

if is_windows():
    INSTALL_LIB_DIR = os.path.abspath(os.path.join(ROOT, ".."))
