# -*-encoding=utf-8 -*-
import ConfigParser, os, shlex, subprocess, sys
    
def setAndroidPathEnv(configObj):
    ndkPath = configObj.get('ANDROID', 'NDK_PATH')
    os.putenv('NDK', ndkPath)
    
    level, arch, toolchainInstallDir = configObj.get('NDK', 'LEVEL'), configObj.get('NDK', 'ARCH'), configObj.get('NDK', 'TOOLCHAIN_INSTALL_DIR')
    toolchainCommand = '$NDK/build/tools/make-standalone-toolchain.sh --platform=android-%(level)s --install-dir=%(install-dir)s --arch=%(arch)s' % {'level':level, 'arch':arch, 'install-dir':toolchainInstallDir}
    subprocess.call(toolchainCommand, shell=True)
    
    os.putenv('ANDROID_STANDALONE_TOOLCHAIN', toolchainInstallDir) 

def getCmakeToolchainFileName(configObj):
    androidCmakePath = configObj.get('ANDROID', 'CMAKE_PATH')
    return '%s/toolchain/android.toolchain.cmake' % androidCmakePath

def cmakeDefineString(key, value):
    return '-D%(key)s=%(value)s' % {'key':key, 'value':value}

def getDefineList(configObj):
    level = configObj.get('NDK', 'LEVEL')
    abi = configObj.get('NDK', 'ARCH_ABI')
    return [cmakeDefineString('CMAKE_TOOLCHAIN_FILE', getCmakeToolchainFileName(configObj)), cmakeDefineString('ANDROID_NATIVE_API_LEVEL', level), cmakeDefineString('ANDROID_ABI', abi)]

def executeCmake(configObj, args):
    command = 'cmake %(defines)s %(args)s' % {'defines':' '.join(getDefineList(configObj)), 'args':' '.join(args)}
    print command
    subprocess.call(command, shell=True)

if __name__ == '__main__':
    if  len(sys.argv) < 2:
        subprocess.call("python android_cmake_build.py [cmake args]", shell=True)
    else:
        configObj = ConfigParser.RawConfigParser()
        configObj.read("config.ini") 
        setAndroidPathEnv(configObj)
        executeCmake(configObj, sys.argv[1:])