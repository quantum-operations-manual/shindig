@echo off
py -3 Tools\run.py generate Shindig
if %ERRORLEVEL%==1 GOTO ERROR
py -3 Tools\run.py compile Shindig
if %ERRORLEVEL%==1 GOTO ERROR
echo Everything is good to go
pause
goto:eof

:ERROR
echo Something went wrong, see above
pause