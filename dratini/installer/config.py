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

# The path to the main executable.
BIN_PATH = PROJECT.name + ".py"

# The name of the `g++` wrapper.
CXX_WRAPPER_NAME = PROJECT.name + "-g++"

# The path to the `g++` wrapper.
CXX_WRAPPER_PATH = "./bin/" + CXX_WRAPPER_NAME

# The directory to install binaries to.
INSTALL_BIN_DIR = ROOT + "/bin"

# The directory to install libraries to.
INSTALL_LIB_DIR = ROOT + "/lib"
