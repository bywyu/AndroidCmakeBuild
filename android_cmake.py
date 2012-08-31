# -*-encoding=utf-8 -*-
import ConfigParser, os, shlex, subprocess, sys

pythonFileAbsDirPath = os.path.dirname( os.path.abspath(__file__) )

    
def setAndroidPathEnv(configObj):
    ndkPath = configObj.get('ANDROID', 'NDK_PATH')
    os.putenv('NDK', ndkPath)
    
    level, arch, toolchainInstallDir = configObj.get('NDK', 'LEVEL'), configObj.get('NDK', 'ARCH'), configObj.get('NDK', 'TOOLCHAIN_INSTALL_DIR')
    toolchainCommand = '$NDK/build/tools/make-standalone-toolchain.sh --platform=android-%(level)s --install-dir=%(install-dir)s --arch=%(arch)s --toolchain=%(toolchain)s' \
    % {'level':level, 'arch':arch, 'install-dir':toolchainInstallDir, 'toolchain':getToolchainName(configObj)}
    subprocess.call(toolchainCommand, shell=True)
    
    os.putenv('ANDROID_STANDALONE_TOOLCHAIN', toolchainInstallDir)

def getToolchainName(configObj):
    arch = configObj.get('NDK', 'ARCH')
    prefixStrList = {'arm':'arm', 'mips':'mipsel', 'x86':'x86'}

    if arch == 'x86':
        return '%s-4.4.3' % prefixStrList.get(arch)
    else:
        return '%s-linux-androideabi-4.4.3' % prefixStrList.get(arch)

def getCmakeToolchainFileName():
    androidCmakePath = os.path.join(pythonFileAbsDirPath, 'android-cmake')
    return '%s/toolchain/android.toolchain.cmake' % androidCmakePath

def cmakeDefineString(key, value):
    return '-D%(key)s=%(value)s' % {'key':key, 'value':value}

def getDefineList(configObj):
    defineList = [('CMAKE_TOOLCHAIN_FILE', getCmakeToolchainFileName()),
                ('ANDROID_NATIVE_API_LEVEL', configObj.get('NDK', 'LEVEL')),
                ('ANDROID_ABI', configObj.get('NDK', 'ARCH_ABI')),
                ('ANDROID', 'ON')]
    return map(lambda (x,y): cmakeDefineString(x,y), defineList)

def executeCmake(configObj, args):
    command = 'cmake %(defines)s %(args)s' % {'defines':' '.join(getDefineList(configObj)), 'args':' '.join(args)}
    print command
    subprocess.call(command, shell=True)

if __name__ == '__main__':
    if  len(sys.argv) < 2:
        print "python android_cmake_build.py [cmake args]"
    else:
        configObj = ConfigParser.RawConfigParser()
        configObj.read( os.path.join(pythonFileAbsDirPath, "config.ini") ) 
        setAndroidPathEnv(configObj)
        executeCmake(configObj, sys.argv[1:])