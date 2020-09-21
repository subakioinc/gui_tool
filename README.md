UAVCAN GUI Tool
===============

[![Travis CI](https://travis-ci.org/UAVCAN/gui_tool.svg?branch=master)](https://travis-ci.org/UAVCAN/gui_tool)
[![Gitter](https://img.shields.io/badge/gitter-join%20chat-green.svg)](https://gitter.im/UAVCAN/general)

UAVCAN GUI Tool은 UAVCAN bus 관리 및 진단을 위한 크로스 플랫폼(Linux/Windows)를 지원하는 어플리케이션이다.

[**uavcan.org/GUI_Tool** 에 있는 문서 읽기](http://uavcan.org/GUI_Tool).

[**forum.uavcan.org** 포럼에 질문하기](https://forum.uavcan.org).

설치 방법 :

- [**LINUX**](#installing-on-linux)
- [**WINDOWS**](#installing-on-windows)
- [**OSX**](#installing-on-osx)

![UAVCAN GUI Tool 화면 캡쳐](screenshot.png "UAVCAN GUI Tool screenshot")

## Linux에 설치하기

간단한 방법 :

1. OS의 패키지 관리자(APT 사용)를 통해서 Python 3용 PyQt5 설치하기
2. PIP를 통해 Git에서 바로 받아서 설치하기:
`pip3 install git+https://github.com/UAVCAN/gui_tool@master`
(이렇게 하면 수동으로 repository를 clone할 필요가 없다.).
또 다른 방법으로, 개발자라면 local copy로 설치를 원하는 경우 `pip3 install .` 을 실행한다.

배포판에 따라서 추가적인 의존성을 설치가 필요할 수도 있다. (아래 참조)

일단 어플리케이션이 설치되면, 데스크탑 메뉴에서 새로운 데스트탑 엔트리가 보인다;
`PATH`에 설정되어`uavcan_gui_tool`로 실행이 가능하다.
만약 데스크탑 환경이 메뉴를 자동으로 업데이트하지 않는다면, 수동으로 해야하며 이때 `sudo update-desktop-database` 를 실행한다.

Matplotlib을 설치하는 것을 추천한다. 어플리케이션 자체에서 사용하지는 않지만 IPython 콘솔을 사용할때 편리하다.

### Debian-based 배포판

```bash
sudo apt-get install -y python3-pip python3-setuptools python3-wheel
sudo apt-get install -y python3-numpy python3-pyqt5 python3-pyqt5.qtsvg git-core
sudo pip3 install git+https://github.com/UAVCAN/gui_tool@master
```

#### 문제 해결

아래와 같은 에러로 설치 실패 시, IPython을 `sudo pip3 install ipython` 명령으로 직접 설치가 가능하다:

> error: Setup script exited with error in ipython setup command:
> Invalid environment marker: sys_platform == "darwin" and platform_python_implementation == "CPython"


## Windows에서 설치하기

In order to install this application,
**download and install the latest `.msi` package from here: <https://files.zubax.com/products/org.uavcan.gui_tool/>**.

### MSI 패키지 만들기


먼저 의존성 설치하기 :

* [WinPython 3.4 or 이후 버전, pre-packaged with PyQt5](http://winpython.github.io/).
터미널에서 `python` 실행시 python이 실행되는지 확인한다. 만약 실행되지 않는다면 `PATH`를 확인한다.
* Windows 10 SDK.
[Visual Studio의 Community 버전을 설치하면서 Windows SDK 설치](https://www.visualstudio.com/).

다음으로 외부 디렉토리에 코드 서명 인증서를 포함하는 `*.pfx` 파일을 위치시킨다.
(빌드 스크립트는 `../*.pfx` 을 검색한다).
여기까지 완료한 후에 다음을 실행한다.(스크립트는 인증서 파일을 읽기 위해서 패스워드 프롬프트가 나타난다):

```dos
python -m pip uninstall -y uavcan
python -m pip uninstall -y uavcan_gui_tool
python setup.py install
python setup.py bdist_msi
```

`dist/` 위치에서 서명된 MSI를 수집하게 된다.

## Development

### Releasing new version

First, deploy the new version to PyPI. In order to do that, perform the following steps:

1. Update the version tuple in `version.py`, e.g. `1, 0`, and commit this change.
2. Create a new tag with the same version number as in the version file, e.g. `git tag -a 1.0 -m v1.0`.
3. Push to master: `git push && git push --tags`

다음으로 위에서 설명한 방법으로 Windows MSI 패키지를 빌드하고 결과로 나온 MSI 파일을 배포 서버에 업로드 시킨다.

### Code style

Please follow the [Zubax Python Coding Conventions](https://kb.zubax.com/x/_oAh).
