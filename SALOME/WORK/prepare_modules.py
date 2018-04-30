#################################################################################
# 
# This script is intended for replacing paths in all *.cmake files in modules 
# of SALOME. 
#
# Usage:
#       prepare_modules.py <native_path>
# where
#       <native_path> is path which will be replaced
#
# Notes:
# - the script is supposed to be run in correct environment
# i.e. *_ROOT_DIR and other important variables are set properly; 
# otherwise the script will fail.
#
################################################################################

import sys
import os
import fnmatch
import fileinput

# Find files recursively in the directory by pattern
def find_files(directory, pattern):
  """
  Find files recursively in the directory by pattern
  """
  for root, dirs, files in os.walk(directory):         
    for basename in files:             
      if fnmatch.fnmatch(basename, pattern):                 
        filename = os.path.join(root, basename)                 
        yield filename         

# Find files recursively in the directory by pattern
# and replace line1 to line2 
def process_files(directory, pattern, line1, line2):
  """
  Find files recursively in the directory by pattern
  and replace line1 to line2 
  """
  for filename in find_files(directory, pattern):
    print "Process file : " + filename
    finput = fileinput.FileInput(filename,inplace=1)
    for line in finput:
      if line[-1].isspace():
      	line = line[:-1]
      line = line.replace(line1,line2)
      print line

# Current SALOME_ROOT_DIRECTORY.
real_path_w = os.path.abspath(os.getenv("SALOME_ROOT_DIR"))
real_path_l = real_path_w.replace("\\", "/")
# Native SALOME_ROOT_DIRECTORY.
native_install_path_w = os.path.abspath(sys.argv[1])
native_install_path_l = native_install_path_w.replace("\\", "/")

all_modules = []
all_modules.append('LIBBATCH')
all_modules.append('KERNEL')  
all_modules.append('GUI')
all_modules.append('GEOM')
all_modules.append('MED')
all_modules.append('MEDCOUPLING')
all_modules.append('SMESH')
all_modules.append('YACS')
all_modules.append('JOBMANAGER')
all_modules.append('PARAVIS')
all_modules.append('HEXABLOCK')
all_modules.append('HEXABLOCKPLUGIN')
all_modules.append('NETGENPLUGIN')
all_modules.append('GHS3DPLUGIN')
all_modules.append('BLSURFPLUGIN')
all_modules.append('HEXOTICPLUGIN')
all_modules.append('COMPONENT')
all_modules.append('CALCULATOR')
all_modules.append('ATOMGEN')
all_modules.append('ATOMIC')
all_modules.append('ATOMSOLV')
all_modules.append('PYCALCULATOR')
all_modules.append('LIGHT')
all_modules.append('PYLIGHT')
all_modules.append('RANDOMIZER')
all_modules.append('SIERPINSKY')
all_modules.append('PYHELLO')
all_modules.append('HELLO')
all_modules.append('HYBRIDPLUGIN')

for sm in all_modules:
  name = sm + '_ROOT_DIR'
  smvar = os.getenv(name)
  if smvar is not None and os.path.exists(smvar) :
    process_files(smvar, "*.cmake", native_install_path_l, real_path_l)
