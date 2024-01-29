# Linux
최초 작성일 : 2024-01-18 
마지막 수정일 : 2024-01-15  
  
## 0. Overview
리늑스(Linux)는 오픈 소스 운영 체제로, 다양한 컴퓨터 시스템 및 장치에 사용되며, 데이터 엔지니어링 분야에도 중요한 역할을 한다. 데이터 엔지니어링은 다중 사용자의 다중 작업이 요구되고, 안정성과 신뢰성, 네트워킹과 웹 서비스과 밀접한 관련이 있다. 그리고 리눅스는 이러한 데이터 엔지니어링의 요구사항을 만족하며, Apache Hadoop, Apache Spark, Apache Kafka 등의 빅데이터 도구는 주로 리눅스 서버에서 실행되기 때문에 리눅스에 대한 학습은 필수적이다.

WSL은 Microsoft가 개발한 Windows 운영 체제에서 리눅스 배포판을 실행할 수 있도록 하는 기술이며, 설치와 세팅이 간단하다는 장점이 있다. 또, Ubuntu는 안정성, 보안성 및 개발자 친화성을 중시하는 운영 체제이며, WSL와 함께 사용하면 Windows에서 리눅스 환경을 편리하게 실행하고 사용할 수 있으며, Windows 및 리눅스 간의 통합된 개발 및 작업 환경을 구성할 수 있다는 장점이 존재한다.

따라서, 본 학습에서는 WSL를 설치하여, 리눅스 환경과 유저를 생성하고, 리눅스 환경에서 작업을 할 수 있는 간단한 명령어에 대해서 공부한다.


## Table of Contents
1. [Installing WSL2 System in Windows](#1.-Installing-WSL2-Sytem-in-Windows)


## 1. Installing WSL2 System in Windows
Windows 환경에서 명령 프롬프트(cmd)를 관리자 권한으로 실행한다. 이 후, **wsl --install**를 입력하고, WSL를 설치한다.한다.

```console
wsl --install
```

## 2. Running Linux and Adding Users   
windows 환경에서 사용자를 만들고, 사용자를 전환하는 것처럼 리눅스에서도 관리자 이외에 사용자를 추가할 수 있다. 사용자는 다음과 같이 추가한다. 사용자를 추가하고도 아무런 글자가 출력되지 않는데, 이어서 비밀번호를 추가적인 'passwd' 명령으로 설정할 수 있다.
```console
root@DESKTOP-EOSJ8EJ:~# sudo useradd example
root@DESKTOP-EOSJ8EJ:~# passwd example
New password:
Retype new password:
passwd: password updated successfully
root@DESKTOP-EOSJ8EJ:~#
```

반대로, 사용하지 않는 사용자는 아래와 같이 삭제할 수 있다.
```console
root@DESKTOP-EOSJ8EJ:~# sudo userdel example
```

리눅스에서는 사용자를 추가하는 명령어가 2가지가 있는데, 하나는 위에서 실습한 'useradd'명령이고, 나머지 하나는 'adduser'명령어이다. 이 둘은 동일하게 사용자를 추가하는 명령어이지만, 'useradd' 명령은 기본적으로 사용자 계정을 추가할 때 필요한 설정만 수행하며 추가적인 작업을 수동으로 해야 하고, 'adduser' 명령은 사용자 계정을 추가할 때 추가적인 설정을 자동으로 처리한다. 위와 달리 아래에서 'adduser' 명령을 통해 다시 한번 사용자를 추가해보자

```console
root@DESKTOP-EOSJ8EJ:~# adduser example
Adding user `example' ...
Adding new group `example' (1003) ...
Adding new user `example' (1003) with group `example' ...
Creating home directory `/home/example' ...
Copying files from `/etc/skel' ...
New password:
Retype new password:
passwd: password updated successfully
Changing the user information for example
Enter the new value, or press ENTER for the default
        Full Name []: Name
        Room Number []: Room
        Work Phone []: 123-123-123
        Home Phone []: 321-321-321
        Other []: etc
Is the information correct? [Y/n] y
root@DESKTOP-EOSJ8EJ:~#
```
앞 'useradd'명령과 다르게 사용자 추가 단계에서 비밀번호, 이름, 연락처 등에 대해 입력을 받고, 입력 받은 정보가 올바른지 확인까지 하는 절차를 갖는다.

리눅스는 windows와 비교하였을 때, 보안성에 대해 더 중점을 둔 운영체제이다. 따라서, 사용자에 따라 파일과 실행에 대한 권한을 별도로 설정해야 하며, 사용자를 추가한 후, 권한에 대한 아무런 설정을 해주지 않으면, 권한 문제로 인해 대부분의 작업을 수행하지 못한다. 학습인 만큼, 만들어진 계정에 권한을 부여해보자. 'sudo visudo' 명령은 리눅스 시스템에서 sudo 권한을 관리하는 sudoers 파일을 편집하는 데 사용된다.

```console
sudo visudo
```

그러면 vi 편집기 내로 이동하는데 '# USER privilege specfication' 아래에 다음과 같이 작성하고, 저장한다.
```console
example ALL=(ALL:ALL) ALL
```

