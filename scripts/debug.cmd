@echo off

SET bin="examples/hello_world"
SET src="%bin%.py"
SET cpp_src="%bin%.cpp"

IF EXIST %cpp_src% del %cpp_src%
python dratini.py %src% -o %cpp_src%
IF EXIST %bin% del %bin%
python dratini.py %src% -o %bin%
./%bin%
