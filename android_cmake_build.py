# -*-encoding=utf-8 -*-
import ConfigParser, os, shlex, subprocess, sys
    
def setAndroidPathEnv(configObj):
    sdkPath, ndkPath = configObj.get('ANDROID', 'SDK_PATH'), configObj.get('ANDROID', 'NDK_PATH')
    os.putenv('ANDROID_NDK', ndkPath)
    #os.putenv('ANDROID_SDK', sdkPath)
    
    level, arch, toolchainInstallDir = configObj.get('NDK', 'LEVEL'), configObj.get('NDK', 'ARCH'), configObj.get('NDK', 'TOOLCHAIN_INSTALL_DIR')
    toolchainCommand = '$ANDROID_NDK/build/tools/make-standalone-toolchain.sh --platform=android-%(level)s --install-dir=%(install-dir)s --arch=%(arch)s' % {'level':level, 'arch':arch, 'install-dir':toolchainInstallDir}
    #subprocess.call(toolchainCommand, shell=True)
    
    #prePath = os.getenv('PATH')
    #os.putenv('PATH', '%s/bin:%s' % (toolchainInstallDir, prePath))
    #os.putenv('CC', getCCName(configObj, arch))
    
    #os.putenv('ANDROID_NDK_TOOLCHAIN_ROOT', toolchainInstallDir)
    #androidCmakePath = configObj.get('ANDROID', 'CMAKE_PATH')
    #os.putenv('ANDTOOLCHAIN', '%s/toolchain/android.toolchain.cmake' % androidCmakePath)
    
    
    
def getCCName(configObj, arch):
    ccNameMap = {'linux':'%s-linux-androideabi-g++' % arch}
    return ccNameMap.get( configObj.get('NDK', 'HOST_SYSTEM') )

def executeCmake(configObj, args):
    androidCmakePath = configObj.get('ANDROID', 'CMAKE_PATH')
    command = 'cmake -DCMAKE_TOOLCHAIN_FILE=%s %s' % ('%s/toolchain/android.toolchain.cmake' % androidCmakePath,  ' '.join(args))
    print command
    subprocess.call(command, shell=True)

if __name__ == '__main__':
    if  len(sys.argv) < 2:
        print 'please input args...'
    else:
        configObj = ConfigParser.RawConfigParser()
        configObj.read("config.ini") 
        setAndroidPathEnv(configObj)
        executeCmake(configObj, sys.argv[1:])