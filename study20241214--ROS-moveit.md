Ubuntu20.04LTS / ROS-noetic

moveit은 지원되는 라이브러리로, 충돌 회피 및 경로 계획을 쉽게 구현할 수 있도록 ROS에서 지원되는 라이브러리이다. 특히, moveit assistance를 이용하면, urdf 파일을 이용하여, 손쉽게 패키지를 작성할 수 있고, 작성한 패키지를 launch 시켜 OPML을 이용하면, 경로 계획을 할 수 있다. 먼저, urdf 파일이 준비되었단 가정 하에 ROS 명령어를 사용하여 urdf 파일을 체크해볼 수 있다. 아래 자료는 Youtube 영상 https://www.youtube.com/watch?v=csaStjYVYtk&ab_channel=KIMeLab을 참고하였다.

1. Write and Check URDF files

```bash
$ ~/catkin_ws/src/testbot_description/urdf$ check_urdf testbot.urdf
robot name is: testbot
---------- Successfully Parsed XML ---------------
root Link: base has 1 child(ren)
    child(1):  link1
        child(1):  link2
            child(1):  link3
                child(1):  link4
```
위 명령어를 통해 로봇의 외관을 결정하는 urdf 파일을 체크해볼 수 있다. 또한, 위 lint와 joint의 관계를 시각적으로도 표현할 수 있다.
``` bash
$ ~/catkin_ws/src/testbot_description/urdf$ urdf_to_graphiz testbot.urdf
Created file testbot.gv
Created file testbot.pdf
```

2. Moveit Setup
아래에서는 기본적으로 ROS, Moveit이 설치 되어 있다는 가정 하에 작업을 수행하는 것이다. 만약 moveit이 설치되어 있지 않다면 아래 코드를 이용하여 moveit 설치한다.

Moveit 패키지 설치
``` bash
$ sudo apt update
$ sudo apt install ros-noetic-moveit*
```

Moveit 설치하고 나서 catkin build를 한번 수행하고, 패키지가 성장적으로 설치 되었는지 확인한다.
``` bash
$ cd ~/catkin_ws & catkin_make
$ source devel/setup.bash
```

빌드가 완료 되었다면, 이제 패키지가 인식되기 때문에 rospack을 이용해서 조회한다.
``` bash
rospack find moveit_setup_assistance
```

위 코드를 이상 없이 실행되고, 패키지가 정상적으로 인식된다면, setup assistance를 실행한다. 이 프로그램도 launch 파일로 구성되어 있기 때문에 roslaunch 명령어를 사용해서 실행하면, GUI 실행된다.

``` bash
$ roslaunch moveit_setup_assistant setup_assistant.launch
```

GUI가 화면에 나타나면, Start에서 URDF 파일을 업로드한다.

Self-Collisions에서는 충돌을 감지하는 matrix를 생성하는 단계이다.

Plannig Group에서는 경로 계획을 할때의 사용되는 group을 설정한다. 매니퓰레이터 로봇의 경우, 대게 robot의 arm과 end-effector를 기준으로 group을 설정한다.

Robot Pose는 





   


