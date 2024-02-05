# AWS-EC2-Cluster
최초 작성일 : 2024-02-05  
마지막 수정일 : 2024-02-05
  
## 0. Overview  
아래 문서에서는 AWS EC2에서 Apache Hadoop, Spark를 설치하고, 1개의 Master(NameNode, Resource manager), 3개의 Worker(DataNode, Node Manager)로 구성된 클러스터를 구축하는 과정을 설명한다.  

Amazon Elastic Compute Cloud (Amazon EC2)는 Amazon Web Services (AWS) 클라우드 플랫폼에서 제공하는 가상 서버 서비스이다. Amazon EC2를 사용하면 필요에 따라 가상 컴퓨팅 리소스를 프로비저닝하고, 운영체제를 선택하며, 애플리케이션을 배포하고 실행할 수 있다. 밑의 설명은 최초 작성일 기준, AWS home의 UI와 Hadoop, Spark 버전을 기준으로 작성한다. 따라서, 얼마든지 UI와 Framework의 버전이 달라질 수 있다는 점을 유의해야 한다. Framework의 버전을 확인하고 설치하는 과정은 뒷 과정에서 별도 설명한다. 아래에는 EC2 위에tj

## Table of Contents
1. [Introduction to Docker](#1.-Introduction-to-Docker)

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
