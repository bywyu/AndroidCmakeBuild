AndroidCmakeBuild
================

# 목적
안드로이드 환경에서 cmake를 이용해 쉽게 빌드할 수 있도록 한다.

# 필요한 프로그램
1. python 2.x

2. android ndk 5~8

# 환경
리눅스 ubuntu 32bit에서만 정상동작을 확인하였다. 64bit일 경우에는 문제가 있으며 다른 환경은 확인되지 않았다.

# 사용법
1. python이 설치되어 있지 않으면 설치하도록 한다. 2.x 버전을 설치해야 하고 2.7.x 버전을 추천한다.

2. android ndk 를 다운로드하여 압축을 풀어 적당한 곳에 위치 시킨다.

3. config.ini 파일의 설정값을 알맞게 변경한다.

[ANDROID]

	NDK_PATH={android ndk가 설치된 디렉토리 경로} ex) ~/android-ndk-r8

[NDK]

	LEVEL={안드로이드 api level} ex) 3,4,5,8,9,14 중 하나

 	ARCH={빌드 CPU 타입} ex) "arm", "x86", "mips" 중 하나

	ARCH_ABI={abi 타입} ex) "armeabi", "armeabi-v7a", "armeabi-v7a with NEON", "armeabi-v7a with VFPV3", "armeabi-v6 with VFP", "x86", "mips" 중 하나

	TOOLCHAIN_INSTALL_DIR={android ndk를 standalone toolchain으로 만들 때 toolchain이 설치될 경로} ex) /home/user/my-android-toolchain

4. "cmake" 대신 "python android_cmake.py"를 사용하여 빌드한다.

	ex) $ cmake ../ => $ python android_cmake.py ../