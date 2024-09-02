echo off

rem set-executionPolicy remoteSigned

pushd %~dp0

python _Run.py %*

pause