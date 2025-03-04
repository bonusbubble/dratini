#!/usr/bin/env bash

# ./scripts/build-generic.sh

bin="examples/hello_world"
src="$bin.py"
cpp_src="$bin.cpp"

clear
sudo python3 installer.py --install
rm -f $cpp_src
python dratini.py $src -o $cpp_src --cxxflags=-O3
rm -f $bin
python dratini.py $src -o $bin --cxxflags=-O3
./$bin
