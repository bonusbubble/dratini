#!/usr/bin/env bash

./scripts/_init.sh

export DRATINI_PLATFORM=$(python3 dratini.py --emit-platform)
export CC=clang
export CXX=clang++

./scripts/_build.sh
