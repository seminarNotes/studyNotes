# AWS-EC2-Cluster
최초 작성일 : 2024-02-05  
마지막 수정일 : 2024-02-05
  
## 0. Overview  
아래 문서에서는 AWS EC2에서 Apache Hadoop, Spark를 설치하고, 1개의 Master(NameNode, Resource manager), 3개의 Worker(DataNode, Node Manager)로 구성된 클러스터를 구축하는 과정을 설명한다.  

Amazon Elastic Compute Cloud (Amazon EC2)는 Amazon Web Services (AWS) 클라우드 플랫폼에서 제공하는 가상 서버 서비스이다. Amazon EC2를 사용하면 필요에 따라 가상 컴퓨팅 리소스를 프로비저닝하고, 운영체제를 선택하며, 애플리케이션을 배포하고 실행할 수 있다. 밑의 설명은 최초 작성일 기준, AWS home의 UI와 Hadoop, Spark 버전을 기준으로 작성한다. 따라서, 얼마든지 UI와 Framework의 버전이 달라질 수 있다는 점을 유의해야 한다. Framework의 버전을 확인하고 설치하는 과정은 뒷 과정에서 별도 설명한다. 아래에는 EC2 위에tj

## Table of Contents
1. [Introduction to Docker](#1.-Introduction-to-Docker)

## 1. Introduction to Docker  

[EC2] 검색 - [인스턴스] - [인스턴스 시작] 
이미지는 Ubuntu Server 20.04 LTS, 64bit(x86) 그리고 Free tier를 사용하기 위해 t2.micro 유형을 선택한다.

[스토리지 구성] 내 사용할 수 있는 root 볼륨이 있는데, 사용자의 조건에 맞게 작성하면 된다. 아래 실습에서는 15GiB를 선택했다.

[이름 및 태그] 내 [추가 태그 추가] 눌러 key, value 값을 지정할 수 있다. (key : value) = (admin : seminarnotes)라 입력하였다.

[네트워크 설정] 내에서 네트워크 설정과 보안 설정을 해야한다. 자신이 사용해야 하는 IP를 설정 해야 하지만, 나는 기본 세팅 그대로를 두고 넘어갔다.

인스턴스 생성의 마지막 단계로, [키 페어(로그인)]을 설정한다. [새 키 페어 생성] 눌러 새로운 key pair를 생성하고,

[키 페어 이름]은 keypair_aws, [키 페어 유형]은 RSA, 프라이빗 키 파일 형식은 .pem으로 지정하여, [키 페어 생성]을 클릭했다.

이 후, 인스턴스가 생성되고, [인스턴스 상태]가 실행 중으로 보이면, 정상적으로 EC2가 생성된 것이다.
