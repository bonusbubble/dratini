#!/usr/bin/env bash

./scripts/build-windows-10.sh

bin="examples/hello_world"
src="$bin.py"
cpp_src="$bin.cpp"

clear
sudo python3 installer.py --install
rm -f $cpp_src
python dratini.py $src -o $cpp_src --cxx=$CXX --cxxflags=-O3
rm -f $bin.exe
python dratini.py $src -o $bin --cxx=$CXX --cxxflags=-O3
