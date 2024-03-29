# Docker
최초 작성일 : 2024-01-15  
마지막 수정일 : 2024-02-05
  
## 0. Overview
현재 docker는 너무 많은 개발자와 유저들이 사용하고 있는 tool이다. 훌륭한 양질의 내용과 콘텐츠로 docker에 대해 소개하고 있는 영상과 글 또한 많이 있지만, 한번쯤은 docker에 대한 내용을 정리해야만 비로소 내 것이 된다는 결심에 이 글에서 docker에 대한 내용을 정리한다. 이 글에서는 docker에 대한 개념, 설치, 간단한 조작 방법에 대해서 공부한다. 

## Table of Contents
1. [Introduction to Docker](#1.-Introduction-to-Docker)
2. [Install Docker Engine on WLS2](#2.-Install-Docker-Engine-on-WLS2)
3. [Basic Docker Commands](#3.-Basic-Docker-Commands) 

## 1. Introduction to Docker  
Docker는 컨테이너화 기술을 기반으로 하는 오픈 소스 플랫폼으로, 애플리케이션을 패키징하고 실행하는 데 활용된다.  Docker는 애플리케이션과 그 의존성을 격리된 환경인 "컨테이너"에 포장하여 이식성을 높이고, 환경 간에 쉽게 배포 및 실행할 수 있다는 장점이 존재한다.

### 1-1. Docker Object
#### 1-1-1. Docker Daemon  
- Docker 컨테이너를 관리하고 실행하는 핵심 배경 프로세스
- Docker API 요청을 수신하고, 이미지, 컨테이너, 리소스, 네트워크 및 불륨과 같은 Docker 객체를 관리
- 컨테이너가 정상적으로 수행될 수 있게 실행 환경 제공
- 컨테이너 빌드, 실행 및 배포와 같이 Docker 클라이언트로 전송된 명령을 실제 실행

#### 1-1-2. Docker Client  
- Docker Client는 Docker 컨테이너와 상호작용하는 사용자 인터페이스를 제공하는 도구 또는 프로그램
- Docker 컨테이너와 이미지를 관리하고, Docker 호스트 또는 Docker Daemon과 통신하여 컨테이너를 관리하고 다양한 Docker 작업을 수행

#### 1-1-3. Docker Desktop  
- Mac, Windows 또는 Linux 환경을 위한 설치하기 쉬운 애플리케이션
- 컨테이너화된 애플리케이션 및 마이크로서비스를 구축하고 공유
- Docker 데몬, Docker 클라이언트, Docker Compose, Docker Content True, Kubernetes 및 Credential Helper가 포함

#### 1-1-4. Docker Resistry  
- Docker 이미지를 저장할 수 있는 원격(remote) 저장소
- Docker 사용자가 실행할 코드가 들어가 있는 바이너리 파일
- Docker는 기본적으로 Docker Hub에서 image를 찾도록 구서

#### 1-1-5. Docker Container
- 컨테이너는 이미지의 실행 가능한 인스턴스
- Docker API 또는 CLI를 사용하여 컨테이너를 생성, 시작, 중지, 이동 또는 삭제 명령
- 컨테이너를 하나 이상의 네트워크에 연결하거나 스토리지를 연결하거나 현재 상태를 기반으로 새 이미지를 생성 가능
- 컨테이너는 생성하거나 시작할 때 제공하는 구성 옵션과 이미지로 정의
- 컨테이너가 제거되면 영구 저장소에 저장되지 않은 상태 변경 사항이 모두 삭제

#### 1-1-6. Docker File
- Docker 이미지를 생성하기 위해 필요한 문서

#### 1-1-7. Docker Engine  
- Docker가 실행되는 계층
- 컨테이너, 이미지, 빌드 등을 관리하는 경량 런타임 및 도구
- Linux 시스템에서 기본적으로 실행


## 2. Install Docker Engine on WLS2
wsl를 통해 home/user 디렉토리로 이동한 다음, 에러를 발생시키는 패키지를 먼저 삭제한다.
```bash
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done
```

설치 전, 설치된 패키지 목록을 최신 상태로 업데이트 한다.
```bash
$ sudo apt-get update
```
이 후, 필요한 패키지를 차례대로 설치한다.
```bash
$ sudo apt-get install ca-certificates curl gnupg
$ sudo install -m 0755 -d /etc/apt/keyrings
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```
아래는 파일에 대한 권한을 변경하는 명령어로, 유저에게 docker.gpg 파일에 대한 읽기 권한을 부여한다.
```bash
$ sudo chmod a+r /etc/apt/keyrings/docker.gpg
```
마지막으로, 저장소를 통해 Docker를 설치하고, 업데이트 할 수 있도록, Docker의 공식 APT 패키지 저장소를 시스템에 추가한다.
```bash
$ echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```
필요한 패키지를 모두 성공적으로 설치하였으면, 최신 상태로 업데이트 한다.
```bash
$ sudo apt-get update
```
아래는 Docker와 관련된 패키지를 설치하는 것으로, docker-ce(Docker Community Edition), docker-ce-cil(Docker Command Line Interface), containerd.io(컨테이너 실행과 관리를 담당하는 런타임), docker-buildx-plugin, docker-compose-plugin(플러그인)을 차례대로 설치한다.
```bash
$ sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```
Docker 프로그램을 실행하는 것으로 다음 명령어를 입력한다.
```bash
sudo service docker start
```
마지막으로, "sudo docker run hello-world"를 입력하여 에러가 발생하지 않으면서, 정상적으로 설치되었음을 확인할 수 있다.
```bash
sudo docker run hello-world
```


## 3. Basic Docker Commands  
### 3-1. Commands for images
Docker는 이미지(image)를 통해 애플리케이션 및 환경을 패키징하고, 이 이미지를 Docker Hub와 같은 Docker 레지스트리에서 다른 사람들과 공유하며, 로컬 머신으로 이미지를 가져와서 컨테이너(container)로 실행하는 구조이다. 또한, 컨테이너 실행 환경을 정의하고 패키징하는 데 사용된다. 

#### 3-1-1. Search images in Docker Registry
검색어(SEARCH_KEYWORD)를 사용하여 이미지를 찾고 해당 이미지의 이름, 설명 등을 확인할 수 있다. 예를 들어, mysql에 대한 이미지를 조회하면 다음과 같은 출력을 확인 할 수 있다.
``` bash
# docker search <SEARCH_KEYWORD>
docker search mysql
```
```
NAME                            DESCRIPTION                                     STARS     OFFICIAL   AUTOMATED
mysql                           MySQL is a widely used, open-source relation…   14767     [OK]
mariadb                         MariaDB Server is a high performing open sou…   5633      [OK]
percona                         Percona Server is a fork of the MySQL relati…   624       [OK]
phpmyadmin                      phpMyAdmin - A web interface for MySQL and M…   928       [OK]
bitnami/mysql                   Bitnami MySQL Docker Image                      106                  [OK]
bitnami/mysqld-exporter                                                         6
cimg/mysql                                                                      2
ubuntu/mysql                    MySQL open source fast, stable, multi-thread…   56
rapidfort/mysql                 RapidFort optimized, hardened image for MySQL   25
rapidfort/mysql8-ib             RapidFort optimized, hardened image for MySQ…   9
google/mysql                    MySQL server for Google Compute Engine          25                   [OK]
rapidfort/mysql-official        RapidFort optimized, hardened image for MySQ…   9
elestio/mysql                   Mysql, verified and packaged by Elestio         0
hashicorp/mysql-portworx-demo                                                   0
bitnamicharts/mysql                                                             0
newrelic/mysql-plugin           New Relic Plugin for monitoring MySQL databa…   1                    [OK]
databack/mysql-backup           Back up mysql databases to... anywhere!         105
linuxserver/mysql               A Mysql container, brought to you by LinuxSe…   41
mirantis/mysql                                                                  0
linuxserver/mysql-workbench                                                     54
vitess/mysqlctld                vitess/mysqlctld                                1                    [OK]
eclipse/mysql                   Mysql 5.7, curl, rsync                          1                    [OK]
drupalci/mysql-5.5              https://www.drupal.org/project/drupalci         3                    [OK]
drupalci/mysql-5.7              https://www.drupal.org/project/drupalci         0
datajoint/mysql                 MySQL image pre-configured to work smoothly …   2                    [OK]
```

#### 3-1-2. Pull images from Docker Registry
Docker 이미지를 Docker 레지스트리에서 로컬 머신으로 다운로드한다. 이미지 이름과 선택적으로 태그를 지정하여 원하는 이미지를 가져올 수 있지만, tag를 생략할 경우, 가장 최신 버전의 image를 가지고 온다.
``` bash
# docker pull <IAMGE_NAME:TAG>
$ docker pull mysql
```

``` bash
Using default tag: latest
latest: Pulling from library/mysql
bce031bc522d: Pull complete
cf7e9f463619: Pull complete
105f403783c7: Pull complete
878e53a613d8: Pull complete
2a362044e79f: Pull complete
6e4df4f73cfe: Pull complete
69263d634755: Pull complete
fe5e85549202: Pull complete
5c02229ce6f1: Extracting [============================>                      ]  35.09MB/62.09MB
7320aa32bf42: Download complete
```

#### 3-1-3. List images in the local environment
로컬 머신에 저장된 모든 Docker 이미지를 나열한다. 이미지 이름, 태그, 이미지 ID 및 크기 정보가 표시된다.
``` bash
docker images
```
```
REPOSITORY       TAG       IMAGE ID       CREATED        SIZE
apache/airflow   2.8.0     d54aa22e50a8   12 days ago    1.77GB
<none>           <none>    f93b870a0896   2 weeks ago    1.77GB
mysql            latest    73246731c4b0   3 weeks ago    619MB
apache/airflow   <none>    3accc302611d   3 weeks ago    1.44GB
mysql            5.7       5107333e08a8   4 weeks ago    501MB
postgres         13        135171763bd4   4 weeks ago    413MB
redis            latest    e40e2763392d   5 weeks ago    138MB
kibana           8.11.1    dd30ec151776   2 months ago   1.04GB
elasticsearch    8.11.1    be606e19dd0f   2 months ago   1.43GB
hello-world      latest    d2c94e258dcb   8 months ago   13.3kB
```
docker를 설치한 후, 정상적으로 설치가 완료되었는지 확인했었던 "hello-world" 이미지, 과어에 공부하기 위해 사용했단 airflow와 kibana에 대한 image도 조회가 된다.

#### 3-1-4. Delete images in the local environment
상황에 따라 로컬 머신에 있는 이미지를 삭제 해야 하는 경우가 있다. 이미지 이름과 태그를 지정하여 특정 이미지를 삭제하거나 혹은 테그 없이 이미지 ID(TARGET_KEYWORD)를 사용해서 이미지를 지정하여 삭제할 수 있다. 예를 들어, hello-world 이미지와 airflow 이미를 삭제해보자.
``` bash
# docker rmi <IMAGE_ID>
docker rmi d2c94e258dcb
```
```
Untagged: hello-world:latest
Untagged: hello-world@sha256:ac69084025c660510933cca701f615283cdbb3aa0963188770b54c31c8962493
Deleted: sha256:d2c94e258dcb3c5ac2798d32e1249e42ef01cba4841c2234249495f87264ac5a
```
이 때, airflow에 대한 이미지 id가 2개로 조회된다. 이미지를 삭제하면, 실행 중인 컨테이너에도 영향을 줄 수 있기 때문에, 삭제하고자 하는 이미지의 id를 확인하고, 정확하게 입력하여 삭제를 하도록 한다. 여기에서는 airflow의 두 이미지 중, tag가 '<none>'으로 되어 있는 이미지 ('3accc302611d')를 삭제하였다. container를 삭제하는 명령어는 'rm'('remove')이지만, 이미지를 삭제하는 명령어는 'rmi'('remove image')인 것에 유의한다.
``` bash
# docker rmi <IMAGE_ID>
docker rmi 3accc302611d
```
```
Untagged: apache/airflow@sha256:54896d94e2b535f18b3ea3edce1c5ff2a205300b2161c8faf163b7f502a092c1
Deleted: sha256:3accc302611d6ba3716d4bae2b7a07bf941f8d5e637a1ae7c1944b4636f21d32
```
삭제 명령 후, 다시 이미지를 조회해보면 삭제한 이미지가 조회되지 않아 정상적으로 삭제 되었음을 확인할 수 있다.
```bash
docker images
```

```
apache/airflow   2.8.0     d54aa22e50a8   12 days ago    1.77GB
<none>           <none>    f93b870a0896   2 weeks ago    1.77GB
mysql            latest    73246731c4b0   3 weeks ago    619MB
mysql            5.7       5107333e08a8   4 weeks ago    501MB
postgres         13        135171763bd4   4 weeks ago    413MB
redis            latest    e40e2763392d   5 weeks ago    138MB
elasticsearch    8.11.1    be606e19dd0f   2 months ago   1.43GB
kibana           8.11.1    dd30ec151776   2 months ago   1.04GB
```
이미지의 history를 조회하는 방법은 아래와 같다
```
docker history [image id]
```

```
$ docker images
REPOSITORY           TAG       IMAGE ID       CREATED         SIZE
tomcat               9.0       2601bdcf2b42   10 days ago     463MB
nginx                latest    b690f5f0a2d5   3 months ago    187MB
openjdk              17        5e28ba2b4cdb   21 months ago   471MB
uifd/ui-for-docker   latest    965940f98fa5   7 years ago     8.1MB

$ docker history 2601bdcf2b42
IMAGE          CREATED       CREATED BY                                      SIZE      COMMENT
2601bdcf2b42   10 days ago   /bin/sh -c #(nop)  CMD ["catalina.sh" "run"]    0B
<missing>      10 days ago   /bin/sh -c #(nop)  ENTRYPOINT []                0B
<missing>      10 days ago   /bin/sh -c #(nop)  EXPOSE 8080                  0B
<missing>      10 days ago   /bin/sh -c set -eux;  nativeLines="$(catalin…   0B
<missing>      10 days ago   /bin/sh -c set -eux;   savedAptMark="$(apt-m…   27.3MB
<missing>      10 days ago   /bin/sh -c #(nop)  ENV TOMCAT_SHA512=06e239d…   0B
<missing>      10 days ago   /bin/sh -c #(nop)  ENV TOMCAT_VERSION=9.0.85    0B
<missing>      10 days ago   /bin/sh -c #(nop)  ENV TOMCAT_MAJOR=9           0B
<missing>      10 days ago   /bin/sh -c #(nop)  ENV GPG_KEYS=48F8E69F6390…   0B
<missing>      10 days ago   /bin/sh -c #(nop)  ENV LD_LIBRARY_PATH=/usr/…   0B
<missing>      10 days ago   /bin/sh -c #(nop)  ENV TOMCAT_NATIVE_LIBDIR=…   0B
<missing>      10 days ago   /bin/sh -c #(nop) WORKDIR /usr/local/tomcat     0B
<missing>      10 days ago   /bin/sh -c mkdir -p "$CATALINA_HOME"            0B
<missing>      10 days ago   /bin/sh -c #(nop)  ENV PATH=/usr/local/tomca…   0B
<missing>      10 days ago   /bin/sh -c #(nop)  ENV CATALINA_HOME=/usr/lo…   0B
<missing>      10 days ago   /bin/sh -c #(nop)  CMD ["jshell"]               0B
<missing>      10 days ago   /bin/sh -c #(nop)  ENTRYPOINT ["/__cacert_en…   0B
<missing>      10 days ago   /bin/sh -c #(nop) COPY file:8b8864b3e02a33a5…   1.18kB
<missing>      11 days ago   /bin/sh -c set -eux;     echo "Verifying ins…   0B
<missing>      11 days ago   /bin/sh -c set -eux;     ARCH="$(dpkg --prin…   308MB
<missing>      11 days ago   /bin/sh -c #(nop)  ENV JAVA_VERSION=jdk-21.0…   0B
<missing>      2 weeks ago   /bin/sh -c set -eux;     apt-get update;    …   50MB
<missing>      2 weeks ago   /bin/sh -c #(nop)  ENV LANG=en_US.UTF-8 LANG…   0B
<missing>      2 weeks ago   /bin/sh -c #(nop)  ENV PATH=/opt/java/openjd…   0B
<missing>      2 weeks ago   /bin/sh -c #(nop)  ENV JAVA_HOME=/opt/java/o…   0B
<missing>      3 weeks ago   /bin/sh -c #(nop)  CMD ["/bin/bash"]            0B
<missing>      3 weeks ago   /bin/sh -c #(nop) ADD file:c646150c866c8b5ec…   77.9MB
<missing>      3 weeks ago   /bin/sh -c #(nop)  LABEL org.opencontainers.…   0B
<missing>      3 weeks ago   /bin/sh -c #(nop)  LABEL org.opencontainers.…   0B
<missing>      3 weeks ago   /bin/sh -c #(nop)  ARG LAUNCHPAD_BUILD_ARCH     0B
<missing>      3 weeks ago   /bin/sh -c #(nop)  ARG RELEASE                  0B
```

#### 3-1-5. Push images to the local environment
image를 통해 하는 마지막 작업은 로컬 머신에서 Docker 레지스트리으로 이미지를 업로드 또는 push를 하는 작업이다. 다른 사람들과 함께 일을 하거나 프로젝트를 하는 경우, image를 구성하여, 공유할 때, 해당 작업을 수행한다.
``` bash
# docker push <IMAGE_NAME:TAG>
docker push mysql:5.7
```

### 3-2. Commands for Containers
Docker는 이미지(image)를 통해 애플리케이션 및 환경을 패키징하고, 이 이미지를 Docker Hub와 같은 Docker 레지스트리에서 다른 사람들과 공유하며, 로컬 머신으로 이미지를 가져와서 컨테이너(container)로 실행하는 구조이다. 따라서, 맨 처음 image에 대한 기본적인 command에 대해서 알아보자.

#### 3-2-1. List Containers
Docker를 나열하는 명령어는 ls(list) 또는 ps(process status)를 사용한다. 두 명령어는 동일한 역할로, Docker 컨테이너를 나열하고 관리하는데 사용되며, 두 명령 모두 실행 중인 Docker 컨테이너 목록을 표시한다. 이 때, container는 생략이 가능하기 때문에 실행 중인 Docker container를 조회하는 명령어는 아래와 같다. 

```bash
docker container ls
docker container ps
docker ls
docker ps
```

한편, 중지된 컨테이너를 포함하여 모든 컨테이너를 표시하도록 하는 명령어는 -a(all)이라는 옵션을 사용하고, 가장 최근에 생성된 컨테이너 순서대로 정렬하는 명령어로는 -l(list)의 옵션을 자주 사용한다. 이들을 이용하여, container의 목록을 표시하기 위한 명령어는 아래와 같다.

```bash
docker container ls -al
docker container ps -al
docker ls -al
docker ps -al
```

#### 3-2-2. Run a Container  
컨테이너를 실행하는 명령어는 docker run 또는 docker start가 있다. 하지만, docker start는 이미 생성된 컨테이너를 실행하는데 반면에, docker run은 새로운 컨테이너를 생성하고 시작하는 명령어이다. 
```bash
# IMAGE_ID만 가능
# 새로운 CONTAINER 인스턴스가 생성
docker run <IMAGE_ID>

# IMAGE_ID / CONTAINER_ID 모두 가능
docker start <IMAGE_ID>
docker start <CONTAINER_ID>
```
docker run <IMAGE_ID>을 사용하면, 기존의 컨테이너를 삭제되지 않고,  이미지 이름을 기반으로 새로운 컨테이너가 생성되고 실행된다. 기존의 컨테이너가 있더라도 새로운 컨테이너 인스턴스를 실행한다. 반면, docker start는 기존의 컨테이너를 실행하기 때문에, IMAGE_ID/CONTAINER_ID를 모두 사용하여, 특정 CONTAINER를 타겟팅하여 실행할 수 있다.

명령어 중, run을 기준으로 실행에 대한 옵션을 설명한다. 백그라운드 모드로 실행하기 위해 -d 명령어를 사용한다.
```bash
docker run -d 
```

한편, 포트를 포워딩하는 옵션으로 -p를 사용할 수 있다. -p 옵션은 호스트 머신의 포트와 컨테이너 내부의 포트를 연결한다. 예를 들어, 호스트의 8080 포트를 컨테이너 내부의 80포트와 연결하여 nginx를 호스트의 8080 포트에서 실행하기 위해 아래와 같은 명령어를 작성한다.
```bash
docker run -p 8080:80 nginx
```


#### 3-2-3. Stop a Container
실행 중인 컨테이너를 종료하는 명령어 중, 유사한 명령어는 stop/kill 명령어이다. stop Docker 컨테이너를 중지하는 데 사용되는 대표적인 명령어이지만, kill의 경우, 컨테이너를 강제/무조건적으로 중지(Terminate)합니다. 컨테이너를 빠르게 중지해야 하는 경우 혹은 docker stop으로 중지되지 않는 경우 kill 명령어를 사용하지만, 강제 중단으로 인한 데이터 손실이 발생할 수 있기 때문에 명령어 사용에 유의 해야 한다.

```bash
docker stop <CONTAINER_ID>

docker kill <CONTAINER_ID>
```
docker ps -q 명령어는 현재 실행 중인 Docker 컨테이너의 컨테이너 ID(또는 짧은 형태의 컨테이너 ID) 목록을 출력하는 명령어로, 이를 변수화($)하면, 실행 중인 모든 컨테이너를 아래와 같이 중지 할 수 있다.
```bash
docker stop $(docker ps -q)

docker kill $(docker ps -q)
```


#### 3-2-4. Remove a Container

컨테이너의 파일 시스템과 설정 정보가 모두 삭제
```
$ docker rm <CONTAINER_ID>
```
#### 3-2-5. Inspace a Container
#### 3-2-6. View Container Logs
#### 3-6-7. Attach to Terminal for Container  
```bash
docker run <CONTAINER_ID>
```
docker 이미지를 사용해서 새로운 컨테이너를 실행하면서, 대화형 터미널로 컨테이너 내부에 연결
```bash
docker attach <CONTAINER_ID>
```

```bash
docker run -it <CONTAINER_ID>
```


## 4. Dockerfile and DockerImage  
### 4-1. Dockerfile  
Dokcerfile 은 코드의 형태로 인프라를 구성하는 방법을 텍스트 형식으로 정의해놓은 파일을 의미한다. 이러한 Dockerfile은 build를 사용하여 Dockerimage를 구성할 수 있다. Dockerfile에는 이미지를 지정하거나 원하는 SW 및 library를 설치하기 위한 명령들을 기술하고, 컨테이너 실행 시 수행할 명령을 기술한다.  가장 기본이 되는 Dockerfile은 다음과 같은 형식을 따른다.  
``` dockerfile
FROM <사용될 이미지 이름>
COPY <container 포함 파일명 대상 경로>
RUN <리눅스 명령어>
...
```
예를 들면, 
``` dockerfile
FROM nginx:lastest
RUN echo '<h1> test nginx web page </h1>' >> index.html
RUN cp /index.html /usr/share/nginx/html
```

dockerfile을 build하는 명령어는 아래와 같다.
``` bash
$ docker build -t <생성할 이미지명>
Dockerfile 위치
docker build -t testserver
```

- tag의 경우, 별도 작성하지 않으면 last[default]으로 자동으로 입력된다.


`
