#!/usr/bin/env bash

./scripts/_init.sh

export DRATINI_PLATFORM=windows-64bit-exe
export CC=i686-w64-mingw32-gcc
export CXX=i686-w64-mingw32-g++

./scripts/_build.sh
