@ECHO OFF

@REM ---------------------------------
@REM Getting absolute path for SALOME ROOT DIRECTORY
@CD %~dp0..
@SET SALOME_ROOT_DIR=%cd%
@CD %~dp0
@REM ---------------------------------

@IF NOT EXIST installation_path.log GOTO MSG
@IF NOT EXIST prepare_products.py GOTO MSG
@set /p PREV_DIR=<installation_path.log
@IF NOT DEFINED PREV_DIR GOTO MSG
@IF "%SALOME_ROOT_DIR%" == "%PREV_DIR%" @GOTO END
@SET list=(LIBBATCH KERNEL GUI GEOM MED MEDCOUPLING SMESH YACS JOBMANAGER PARAVIS HEXABLOCK HEXABLOCKPLUGIN NETGENPLUGIN GHS3DPLUGIN HEXOTICPLUGIN BLSURFPLUGIN ATOMGEN ATOMIC ATOMSOLV PYCALCULATOR CALCULATOR COMPONENT LIGHT PYLIGHT RANDOMIZER SIERPINSKY PYHELLO HELLO HYBRIDPLUGIN)

@REM ---------------------------------
@SET PDIR=%SALOME_ROOT_DIR%\PRODUCTS
@IF NOT EXIST "%PDIR%\env_compile.bat" GOTO C1
@ECHO Preparing third-party products for SALOME:
@call "%PDIR%\env_compile.bat"
@CALL %PYTHONBIN% "%~dp0prepare_products.py" "%PREV_DIR%"
@ECHO Preparing modules of SALOME:
@for %%i in %list% do ( 
  @SET %%i_ROOT_DIR=%SALOME_ROOT_DIR%\MODULES\%%i\RELEASE\%%i_INSTALL
)
@CALL %PYTHONBIN% "%~dp0prepare_modules.py" %PREV_DIR%
:C1

@SET PDIR=%SALOME_ROOT_DIR%\PRODUCTSD
@IF NOT EXIST "%PDIR%\env_compile.bat" GOTO C2
@ECHO Preparing third-party products for SALOME:
@call "%PDIR%\env_compile.bat"
@CALL %PYTHONBIN% "%~dp0prepare_products.py" "%PREV_DIR%"
@ECHO Preparing modules of SALOME:
@for %%i in %list% do ( 
  @SET %%i_ROOT_DIR=%SALOME_ROOT_DIR%\MODULES\%%i\RELEASE\%%i_INSTALL
)
@CALL %PYTHONBIN% "%~dp0prepare_products.py" "%PREV_DIR%"
:C2
@REM ---------------------------------

@ECHO %SALOME_ROOT_DIR%>installation_path.log

@GOTO END

:MSG
@ECHO ERROR! There is no information about previous placement of prerequisite products for SALOME! 
@ECHO May be problems with compilation or/and using SALOME as third-party product.
@ECHO Please, check existing of %~dp0installation_path.log, %~dp0prepare_products.bat and try again!

:END
@EXIT