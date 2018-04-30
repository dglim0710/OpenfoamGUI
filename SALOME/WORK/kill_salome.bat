@ECHO OFF

@CALL "%~dp0\set_env.bat"
@CALL "%PDIR%\env_launch.bat"

IF "%SALOME_ROOT_DIR%"=="" (
  GOTO END
)

IF "%HOME%"=="" (
  GOTO END
)

set SALOME_VERBOSE=0
%PYTHONBIN% "%KERNEL_ROOT_DIR%\bin\salome\killSalome.py"

:END
