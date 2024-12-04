



junhuiwoo@WOO-20:~/catkin_ws/src/testbot_description/urdf$ check_urdf testbot.urdf
robot name is: testbot
---------- Successfully Parsed XML ---------------
root Link: base has 1 child(ren)
    child(1):  link1
        child(1):  link2
            child(1):  link3
                child(1):  link4

위 명령어를 통해 로봇의 외관을 결정하는 urdf 파일을 체크할 수 있다.



junhuiwoo@WOO-20:~/catkin_ws/src/testbot_description/urdf$ urdf_to_graphiz testbot.urdf
Created file testbot.gv
Created file testbot.pdf

위 명령어를 통해 urdf의 파일의 흐름을 확인할 수 있다.

[testbot.pdf](https://github.com/user-attachments/files/18003959/testbot.pdf)



junhuiwoo@WOO-20:~$ roslaunch testbot_description testbot.launch
... logging to /home/junhuiwoo/.ros/log/ca4730d8-b20f-11ef-94d0-010fe7e6a182/roslaunch-WOO-20-38420.log
Checking log directory for disk usage. This may take a while.
Press Ctrl-C to interrupt
Done checking log file disk usage. Usage is <1GB.

started roslaunch server http://localhost:33495/

SUMMARY
========

PARAMETERS
 * /robot_description: <?xml version="1....
 * /rosdistro: noetic
 * /rosversion: 1.17.0
 * /use_gui: True

NODES
  /
    joint_state_publisher (joint_state_publisher/joint_state_publisher)
    robot_state_publisher (robot_state_publisher/robot_state_publisher)

auto-starting new master
process[master]: started with pid [38428]
ROS_MASTER_URI=http://localhost:11311

setting /run_id to ca4730d8-b20f-11ef-94d0-010fe7e6a182
process[rosout-1]: started with pid [38438]
started core service [/rosout]
process[joint_state_publisher-2]: started with pid [38441]
process[robot_state_publisher-3]: started with pid [38443]



junhuiwoo@WOO-20:~$ rviz
[ INFO] [1733296680.851667894]: rviz version 1.14.25
[ INFO] [1733296680.851717157]: compiled against Qt version 5.12.8
[ INFO] [1733296680.851731745]: compiled against OGRE version 1.9.0 (Ghadamon)
[ INFO] [1733296680.857449465]: Forcing OpenGl version 0.
[ INFO] [1733296681.202900824]: Stereo is NOT SUPPORTED
[ INFO] [1733296681.202936868]: OpenGL device: NV167
[ INFO] [1733296681.202988431]: OpenGl version: 4.3 (GLSL 4.3) limited to GLSL 1.4 on Mesa system.




