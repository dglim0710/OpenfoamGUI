@ECHO OFF

call "%~dp0\set_env.bat"
echo "%PDIR%
call "%PDIR%\env_launch.bat"

IF "%SALOME_ROOT_DIR%"=="" (
  GOTO END
)

IF "%HOME%"=="" (
  GOTO END
)
SET SALOME_VERBOSE=0

start %PYTHONBIN% "%KERNEL_ROOT_DIR%\bin\salome\envSalome.py" "%PYTHONBIN%" "%KERNEL_ROOT_DIR%\bin\salome\runSalome.py" %* 

:END