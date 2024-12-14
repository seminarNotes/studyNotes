moveit은 지원되는 라이브러리로, 충돌 회피 및 경로 계획을 쉽게 구현할 수 있도록 ROS에서 지원되는 라이브러리이다. 특히, moveit assistance를 이용하면, urdf 파일을 이용하여, 손쉽게 패키지를 작성할 수 있고, 작성한 패키지를 launch 시켜 OPML을 이용하면, 경로 계획을 할 수 있다. 먼저, urdf 파일이 준비되었단 가정 하에 ROS 명령어를 사용하여 urdf 파일을 체크해볼 수 있다.


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



