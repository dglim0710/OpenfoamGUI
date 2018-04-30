#################################################################################
# 
# This script is intended for replacing paths in all *.cmake, 
# *.bat files in third-party products.
#
# Usage:
#       prepare_products.py <native_path>
# where
#       <native_path> is path which will be replaced
#
# Notes:
# - the script is supposed to be run in correct environment
# i.e. PROD_DIR, *_ROOT_DIR and other important variables are set properly; 
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

#Real products install directory
real_product_dir_w = os.path.abspath(os.getenv("PDIR"))
real_product_dir_l = real_product_dir_w.replace("\\", "/")

# Process all "*.cmake" files in third-party products
for prod in ['MEDFILE', 'PARAVIEW', 'HDF5']:
  prodvar = os.getenv("%s_ROOT_DIR"%(prod))
  if os.path.exists(prodvar) :
    process_files(prodvar, "*.cmake", native_install_path_l, real_path_l)

# Process pyqtconfig.py and all "*.bat" files in the pyqt third-party lib
pyqt_dir = os.getenv("PYQT5_ROOT_DIR")
if os.path.exists(pyqt_dir) :
  process_files(pyqt_dir, "*.bat", native_install_path_w, real_path_w)
  # Process  "pyqtconfig.py" file
  process_files(pyqt_dir, "pyqtconfig.py", native_install_path_w.replace("\\","\\\\"), real_path_w.replace("\\","\\\\"))

#Process all *script.py files in the sphinx third-party library
sphinx_dir = os.getenv("SPHINX_ROOT_DIR")
if os.path.exists(sphinx_dir) :
  process_files(sphinx_dir, "*script.py", native_install_path_w, real_path_w)

for prod in ['DOCUTILS']:
  prodvar = os.getenv("%s_ROOT_DIR"%(prod))
  if os.path.exists(prodvar) :
    process_files(prodvar, "*.py", native_install_path_w, real_path_w)
   
# Process sipconfig.py file in the sip third-party lib
sip_dir = os.getenv("SIP_ROOT_DIR")
if os.path.exists(sip_dir) :
  process_files(sip_dir, "sipconfig.py", native_install_path_w.replace("\\","\\\\"), real_path_w.replace("\\","\\\\"))
