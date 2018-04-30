import sys
import fileinput
import fnmatch
import os

all_modules = []
all_modules.append('LIBBATCH')
all_modules.append('KERNEL')  
all_modules.append('GUI')
all_modules.append('GEOM')
all_modules.append('MEDCOUPLING')
all_modules.append('MED')
all_modules.append('SMESH')
all_modules.append('YACS')
all_modules.append('JOBMANAGER')
all_modules.append('PARAVIS')
all_modules.append('HEXABLOCK')
all_modules.append('HEXABLOCKPLUGIN')
all_modules.append('NETGENPLUGIN')
all_modules.append('GHS3DPLUGIN')
#!!!!!!!!!!! GHS3DPRLPLUGIN module has been excluded upon the request of CEA !!!!!!!!!!!
#all_modules.append('GHS3DPRLPLUGIN')
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

def printHelp():
    print "Usage: compile.bat [MODULE1 MODULE2 ... MODULEN]"
    print "MODULE1, MODULE2 ... MODULEN:  modules to build (optional parameters)"
    print "By default all modules will be compiled."
    
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
    
mode = os.getenv("BUILD_MODE")

if not mode in ["Release", "Debug"]:
    print "Wrong compile mode is set: %s. Only Release or Debug mode is allowed." % mode
    print "Refer to the set_env.bat script."
    sys.exit(1)

arch = os.getenv("ARCH")
msvc_exe = os.getenv("msvc_exe")

if len(sys.argv) > 1:
    modules = []
    for m in all_modules:
       if m in sys.argv[1:]: modules.append(m)
       pass
    pass
else:
    modules = all_modules
    pass

if len(modules) < 1:
    print "Nothing to build. Bye..."
    sys.exit(0)
    
for module in modules:
    print "Building module %s in %s" % ( module, mode )
    os.chdir("..\MODULES\%s"%(module.upper()))
    # --
    m = module
    installdir = os.getenv("%s_ROOT_DIR"%(module))
        
    build_dir = os.getenv("%s_BUILD_DIR"%(module))
    src_dir = os.getenv("%s_SRC_DIR"%(module))   

    os.system('mkdir "%s" > dummy 2>&1'%(build_dir))
    os.system('del dummy')

    appendix=''
    if arch == 'Win64':
      appendix=' Win64'

    os.chdir(build_dir)
    cmd  = r'cmake '
    cmd += r'-DCMAKE_INSTALL_PREFIX="%s" '%(installdir)
    cmd += r'-DCMAKE_BUILD_TYPE=%s '%(mode)
    cmd += r'-G "Visual Studio 10%s" '%(appendix)
    if module == "GUI":
       cmd += r'-DSALOME_BUILD_WITH_QT5:BOOL=ON '
       pass
    if module == "GEOM":
       cmd += r'-DSALOME_GEOM_USE_OPENCV:BOOL=ON '
       pass
    if module == "SIERPINSKY":
       cmd += r'-DSALOME_SIERPINSKY_USE_LIBGD:BOOL=OFF '
       pass
    if module == "KERNEL":
       cmd += r'-DSALOME_USE_LIBBATCH:BOOL=ON '
       pass
    if module == "SMESH":
       cmd += r'-DSALOME_SMESH_USE_CGNS=ON '
       cmd += r'-DSALOME_SMESH_USE_TBB=OFF '
       pass
    if module == "MEDCOUPLING":
       cmd += r'-DMEDCOUPLING_ENABLE_PARTITIONER=OFF '
    cmd += r'"%s"'%(src_dir)   
    os.system(cmd)
    print "%s"%(cmd)
    os.system('mkdir "%s" > dummy 2>&1'%(installdir))
    os.system("del dummy")

    vc_arch = arch
    if arch == 'Win64':
      vc_arch = 'x64'

    cmd1 = ""
    if module in ["MEDCOUPLING", "LIBBATCH"]:
       cmd1 = r'cd "%s" && call %s %s.sln /build "%s|%s" /project INSTALL.vcxproj /projectconfig "%s|%s" /out devenv_%s.txt'%(build_dir,msvc_exe,module,mode,vc_arch,mode,vc_arch,module)
    else:    
       cmd1 = r'cd "%s" && call %s SALOME%s.sln /build "%s|%s" /project INSTALL.vcxproj /projectconfig "%s|%s" /out devenv_%s.txt'%(build_dir,msvc_exe,module,mode,vc_arch,mode,vc_arch,module)
    print "%s"%(cmd1)
    os.system(cmd1)

    os.chdir("..\..\..\..\WORK")