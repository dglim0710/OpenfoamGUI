@echo off

IF NOT EXIST "%VS100COMNTOOLS%..\..\VC\vcvarsall.bat" GOTO ERROR1

cd "%~dp0"
call "%~dp0\set_env.bat"
call "%PDIR%\env_compile.bat"

IF "%ARCH%" == "Win64" (
  call "%VS100COMNTOOLS%..\..\VC\vcvarsall.bat" x64
) ELSE (
  IF "%ARCH%" == "Win32" (
    call "%VS100COMNTOOLS%..\..\VC\vcvarsall.bat" x86
  ) ELSE (
    echo Wrong architecture is used. Win32 or Win64 architecture is allowed only.
    echo Refer to the set_env.bat script.
  )
)

rem Launch Visual Studio - either professional (devenv) or Express, as available
if exist "%VS100COMNTOOLS%..\IDE\devenv.exe"  (
  SET msvc_exe=devenv
) else if exist "%VS100COMNTOOLS%..\IDE\VCExpress.exe"  (
  SET msvc_exe=VCExpress
) else (
  GOTO ERROR1
)

%PYTHONBIN% compile.py %*
GOTO END

:ERROR1
ECHO "Visual Studio environment file is not found."
:END