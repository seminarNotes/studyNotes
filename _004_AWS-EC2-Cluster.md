# AWS-EC2-Cluster
최초 작성일 : 2024-02-05  
마지막 수정일 : 2024-02-05
  
## 0. Overview  
아래 문서에서는 AWS EC2에서 Apache Hadoop, Spark를 설치하고, 1개의 Master(NameNode, Resource manager), 3개의 Worker(DataNode, Node Manager)로 구성된 클러스터를 구축하는 과정을 설명한다.  

Amazon Elastic Compute Cloud (Amazon EC2)는 Amazon Web Services (AWS) 클라우드 플랫폼에서 제공하는 가상 서버 서비스이다. Amazon EC2를 사용하면 필요에 따라 가상 컴퓨팅 리소스를 프로비저닝하고, 운영체제를 선택하며, 애플리케이션을 배포하고 실행할 수 있다. 밑의 설명은 최초 작성일 기준, AWS home의 UI와 Hadoop, Spark 버전을 기준으로 작성한다. 따라서, 얼마든지 UI와 Framework의 버전이 달라질 수 있다는 점을 유의해야 한다. Framework의 버전을 확인하고 설치하는 과정은 뒷 과정에서 별도 설명한다. 아래에는 EC2 위에tj

## Table of Contents
1. [Set up on AWS](#1.-Set-up-on-AWS)
2. [SSH and Host Configuration](#2.-SSH-and-Host-Configuration)

## 1. Introduction to Docker  

[EC2] 검색 - [인스턴스] - [인스턴스 시작] 
이미지는 Ubuntu Server 20.04 LTS, 64bit(x86) 그리고 Free tier를 사용하기 위해 t2.micro 유형을 선택한다.

[스토리지 구성] 내 사용할 수 있는 root 볼륨이 있는데, 사용자의 조건에 맞게 작성하면 된다. 아래 실습에서는 15GiB를 선택했다.

[이름 및 태그] 내 [추가 태그 추가] 눌러 key, value 값을 지정할 수 있다. (key : value) = (admin : seminarnotes)라 입력하였다.

[네트워크 설정] 내에서 네트워크 설정과 보안 설정을 해야한다. 자신이 사용해야 하는 IP를 설정 해야 하지만, 나는 기본 세팅 그대로를 두고 넘어갔다.

인스턴스 생성의 마지막 단계로, [키 페어(로그인)]을 설정한다. [새 키 페어 생성] 눌러 새로운 key pair를 생성하고,

[키 페어 이름]은 keypair_aws, [키 페어 유형]은 RSA, 프라이빗 키 파일 형식은 .pem으로 지정하여, [키 페어 생성]을 클릭했다.

이 후, 인스턴스가 생성되고, [인스턴스 상태]가 "대기 중"에서 "실행 중"으로 변경되면, 정상적으로 EC2가 생성/실행된 것이다.



## 2. SSH and Host Configuration


ssh conf 파일을 수정해서, 지정한 hostname으로 쉽게 서버를 접속할 수 있게 세팅한다. 먼저, 키를 관리하고 보관할 수 있는 디렉터리를 하나 생성하고 다운로드 받은 키를 해당 디렉터리에 이동시킨다.
``` bash
$ mkdir -p ~/identity

$ cd ~/identity
```
해당 키를 너무 오픈 되어 있으면, 취약 진단으로 작업에 장애가 생길 수 있기 때문에 change mode를 실행한다.
``` bash
$ chmod 600 keypair_aws.pem
```
ssh-kygen으로 ssh key를 생성한다.
``` bash
$ ssh-keygen
```
~/.ssh 디렉터리에 정상적으로 공개키(pub)가 생성되었음을 확인할 수 있다.
``` bash
$ ls -ltrh ~/.ssh
```
해당 경로에 config 파일을 vim을 통해 파일을 연다.
``` bash
$ cd ~/.ssh

$ sudo vim config
```
Host에는 호출명, HostName에는 Public IP, User에는 ubuntu, IdentiyFile에는 pem 파일의 경로를 작성한다.

``` config
Host master
  HostName [PUBLIC KEY]
  User ubuntu
  IdentityFile ~/identity/keypair_aws.pem
```
작성 후 파일을 저장하고, 파일 권한을 변경한다.
``` bash
$ chmod 440 ~/.ssh/config
```
이 후, master라는 hostname을 통해, 서버에 접속할 수 있는지 hostname을 호출하여, 해당 서버(인스턴스)에 접속한다.
``` bash
$ ssh master
```
ip addr를 통해, AWS 내 instance에 있는 private ip가 동일한지 확인하고, 아무 문제 없다면, 필요한 Framework를 설치할 준비를 한다.
``` bash
# private ip 확인
$ ip addr

$ sudo apt-get -y update
$ sudo apt-get -y upgrade
$ sudo apt-get -y dist-upgrade
```

필요한 라이브러리부터 설치한다.
``` bash
$ sudo apt-get install -y vim
$ sudo apt-get install -y wget
$ sudo apt-get install -y unzip

$ sudo apt-get install -y ssh
$ sudo apt-get install -y openssh-*
$ sudo apt-get install -y net-tools
```

hadoop과 spark는 자바를 기반으로 만들어진 프레임워크이기 때문에 필수적으로 java가 설치되어 있어야 한다. 설치된 이후에는 자바의 버전을 확인한다.
``` bash
sudo apt-get install -y oepnjdk-8-jdk

$ java -version
```

[여기까지 작성했습니다.] ////



shift + g

AWS EC2 - Aphace hadoop, spark cluster 구축


``` bash
$ sudo vim /usr/local/hadoop/etc/hadoop/core-site.xlm
```


``` xml
<configuration>
    <property>
            <name>fs.default.name</name>
            <value>hdfs://mastet:9000</value>
    </property>
</configuration>
```


``` bash
$ sudo vim /usr/local/hadoop/etc/hadoop/hdfs-site.xlm
```
``` xml
<configuration>
    <property>
        <name>dfs.replication</name>
        <value>3</value>
    </property>
    <property>
        <name>dfs.namenode.name.dir</name>
        <value>file:///hdfs_dir/nameNode</value>
    </property>
    <property>
        <name>dfs.datanode.data.dir</name>
        <value>file:///hdfs_dir/dataNode</value>
    </property>
    <property>
        <name>dfs.namenode.secondary.http-address</name>
        <value>worker01:50090</value>
    </property>
</configuration>
```


``` bash
$ sudo vim /usr/local/hadoop/etc/hadoop/yarn-site.xlm
```
``` xml
<configuration>
    <!-- Site specific YARN configuration properties -->
    <property>
        <name>yarn.nodemanager.local-dirs</name>
        <value>file:///hdfs_dir/yarn/local</value>
    </property>
    <property>
        <name>yarn.nodemanager.log-dirs</name>
        <value>file:///hdfs_dir/yarn/logs</value>
    </property>
    <property>
        <name>yarn.resourcemanager.hostname</name>
        <value>master</value>
    </property>
</configuration>
```

```bash
$ sudo vim /usr/local/hadoop/etc/hadoop/mapred-site.xlm
```
``` xml
<configuration>
    <property>
    <!-- mapreduce framework named as yarn -->
        <name>mapreduce.framework.name</name>
        <value>yarn</value>
    </property>
</configuration>
```

```bash
$ sudo vim /usr/local/hadoop/etc/hadoop/hadoop-env.sh
```

``` sh
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export HDFS_NAMENODE_USER="root"
export HDFS_DATANODE_USER="root"
export HDFS_SECONDARYNAMENOTE_USER="root"
export YARN_RESOURCEMANAGER_USER="root"
export YARN_NODEMANAGER_USER="root"
```




스파크 환경설정

spark는 /usr/local/spark/conf$로 이동했을 때, 모든 conf가 template으로 구성되어 있다. 그래서 바로 수정하지 않고, 해당 template를 복사한다.

``` bash
$ sudo cp spark-defaults.conf.template spark-defaults.conf
$ suco vim spark-defaults.conf
```
``` conf
spark.master                yarn
spark.eventLog.enabled      true
spark.eventLog.dir          hdfs://namenode:8021/spark_enginelog
```


``` bash
$ sudo cp spark-env.sh.template spark-env.sh
$ sudo vim spark-env.sh
```

``` sh
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export SPARK_MASTER_HoST=master
export HADOOP_HOME=/usr/local/hadoop
export YARN_CONF_DIR=$HADOOP_HOME/etc/hadoop
export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
```

인스턴스 >> 작업 >> 이미지 및 템플릿 >> 이미지 생성

이미지 이름 :  spark_hadoop_base
이미 설명 : spark_hadoop


Amazon Machine Images(AMI)
이미지 >> AMI

AMI로 인스턴스 시작

다른 설정은 모두 동일하지만

키 페어(로그인)의 경우, 맨 처음 생성하였던 키 페어 "spark_hadoop_aws"를 선택
이 후, [인스턴스 시]

[이미지] >> [AMI]



``` bash 
cd ~/.ssh
ls -ltrh
sudo vim config
```
여기서 ssh와 관련된 설정 



``` bash
sudo hostnamectl set-hostname master
hostname
>> master

sudo sudo vim /etc/hosts
```

각 worker의 inet ip를 작성한다. 서버끼리 통신할 때는 public ip가 아닌 private ip를 사용한다.


``` cong
ip addr


```

``` bash
sudo hostnamectl set-hostname worker01
```
``` bash
sudo hostnamectl set-hostname worker02
```
``` bash
sudo hostnamectl set-hostname worker03
```
이름을 다 변경하고, 각 터미널에 hosts 파일 수정

``` bash
sudo vim /etc/hosts
```








############# docker
리눅스의 응용 프로그램들을 SW 컨테이너 내에서 배치하는 작업을 자동화 하는 오픈 소스 프로젝트  

client와 server 아키텍처



