@echo off

SET PYTHON=python

SET dir=%~dp0

SET project_name=dratini

SET lib_dir=%dir%\..\lib\%project_name%

SET script_path=%lib_dir%\%project_name%.py

%PYTHON% %script_path% %*
