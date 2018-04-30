@echo off

IF NOT EXIST "%VS100COMNTOOLS%..\..\VC\vcvarsall.bat" GOTO ERROR1

call "%~dp0\set_env.bat"
call "%PDIR%\env_compile.bat"

IF "%BUILD_MODE%" == "Debug" (
  echo Debug mode is chosen!
) ELSE (
  IF "%BUILD_MODE%" == "Release" (
    echo Release mode is chosen!
  ) ELSE (
    echo Wrong build mode is used. Debug or Release mode is allowed only.
    echo Refer to the set_env.bat script.
    goto END
  )
)

@REM appendix variable will be used for generation makefile generator-name
IF "%ARCH%" == "Win64" (
  call "%VS100COMNTOOLS%..\..\VC\vcvarsall.bat" x64
  SET appendix="Visual Studio 10 Win64"  
) ELSE (
  IF "%ARCH%" == "Win32" (
    call "%VS100COMNTOOLS%..\..\VC\vcvarsall.bat" x86
    SET appendix="Visual Studio 10"
  ) ELSE (
    echo Wrong architecture is used. Win32 or Win64 architecture is allowed only.
    echo Refer to the set_env.bat script.
  )
)

echo Generation of VC projects for %1 module in %BUILD_MODE% mode for %ARCH%

IF "%1" == "SIERPINSKY" (
  setlocal ENABLEDELAYEDEXPANSION
    cd "!%1_BUILD_DIR!" && cmake -G !appendix! -DCMAKE_INSTALL_PREFIX="!%1_ROOT_DIR!" -DCMAKE_BUILD_TYPE=%BUILD_MODE% -DSALOME_SIERPINSKY_USE_LIBGD:BOOL=OFF "!%1_SRC_DIR!"
  endlocal
 goto END
) 

IF "%1" == "GEOM" (
  setlocal ENABLEDELAYEDEXPANSION
    cd "!%1_BUILD_DIR!" && cmake -G !appendix! -DCMAKE_INSTALL_PREFIX="!%1_ROOT_DIR!" -DCMAKE_BUILD_TYPE=%BUILD_MODE% -DSALOME_GEOM_USE_OPENCV:BOOL=ON "!%1_SRC_DIR!"
  endlocal
 goto END
) 

IF "%1" == "GUI" (
  setlocal ENABLEDELAYEDEXPANSION
    cd "!%1_BUILD_DIR!" && cmake -G !appendix! -DCMAKE_INSTALL_PREFIX="!%1_ROOT_DIR!" -DCMAKE_BUILD_TYPE=%BUILD_MODE% -DSALOME_BUILD_WITH_QT5:BOOL=ON "!%1_SRC_DIR!"
  endlocal
 goto END
) 

IF "%1" == "SMESH" (
  setlocal ENABLEDELAYEDEXPANSION
    cd "!%1_BUILD_DIR!" && cmake -G !appendix! -DCMAKE_INSTALL_PREFIX="!%1_ROOT_DIR!" -DCMAKE_BUILD_TYPE=%BUILD_MODE% -DSALOME_SMESH_USE_CGNS=ON -DSALOME_SMESH_USE_TBB=OFF "!%1_SRC_DIR!"
  endlocal
 goto END
) 

IF "%1" == "MEDCOUPLING" (
  setlocal ENABLEDELAYEDEXPANSION
    cd "!%1_BUILD_DIR!" && cmake -G !appendix! -DCMAKE_INSTALL_PREFIX="!%1_ROOT_DIR!" -DCMAKE_BUILD_TYPE=%BUILD_MODE% -DMEDCOUPLING_ENABLE_PARTITIONER=OFF "!%1_SRC_DIR!"
  endlocal
 goto END
) 

setlocal ENABLEDELAYEDEXPANSION
  cd "!%1_BUILD_DIR!" && cmake -G !appendix! -DSALOME_CMAKE_DEBUG=ON -DCMAKE_INSTALL_PREFIX="!%1_ROOT_DIR!" -DSALOME_CMAKE_DEBUG=ON -DCMAKE_BUILD_TYPE=%BUILD_MODE% "!%1_SRC_DIR!"
endlocal
goto END    

:ERROR1
ECHO "Visual Studio environment file is not found."
:END