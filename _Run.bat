echo off

rem set-executionPolicy remoteSigned

pushd %~dp0

..\python_embeded\python.exe -s _Run.py %*

pause