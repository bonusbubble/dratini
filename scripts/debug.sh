#!/usr/bin/env bash

bin="examples/hello_world"
src="$bin.py"
cpp_src="$bin.cpp"

clear
sudo python3 installer.py --install
rm -f $cpp_src
python dratini.py $src -o $cpp_src
rm -f $bin
python dratini.py $src -o $bin
./$bin
