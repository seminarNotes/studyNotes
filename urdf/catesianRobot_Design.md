URDF로 설계된 이 로봇은 공장과 같은 산업 현장에서 용접(welding) 작업을 수행하도록 디자인되었다. 특히, 로봇은 XYZ 축을 따라 엔드 이펙터(end-effector)를 이동시킬 수 있으며, Z축 방향으로 엔드 이펙터의 끝부분을 제어하기 위해 Roll과 Pitch 각도를 조정할 수 있는 회전 모듈이 추가되었다. 아래는 로봇의 전체적인 구조와 각 제어에 따른 움직임을 보여준다.

```bash
$ check_urdf cartesian_robot.urdf.xacro
robot name is: custom_cartesian_robot
---------- Successfully Parsed XML ---------------
root Link: world has 1 child(ren)
    child(1):  base_link
        child(1):  Column_1
            child(1):  rail_col1_col4
                child(1):  y_axis_controller
                    child(1):  x_axis_rail
                        child(1):  x_axis_controller
                            child(1):  z_axis_rail
                                child(1):  z_axis_revoluate
                                    child(1):  end_effector_cylinder
                                        child(1):  red_end_effector
        child(2):  Column_2
            child(1):  rail_col2_col3
        child(3):  Column_3
        child(4):  Column_4
```

### 1. 전체적인 모습

![no-moving](https://raw.githubusercontent.com/seminarNotes/studyNotes/main/gif/no-moving.gif
)

### 2. x축 평행이동

![no-moving](https://raw.githubusercontent.com/seminarNotes/studyNotes/main/gif/x-axis-moving.gif
)

### 3. y축 평행이동

![no-moving](https://raw.githubusercontent.com/seminarNotes/studyNotes/main/gif/y-axis-moving.gif
)

### 4. z축 평행이동

![no-moving](https://raw.githubusercontent.com/seminarNotes/studyNotes/main/gif/z-axis-moving.gif
)

### 5. end-effector 각도 제어

![no-moving](https://raw.githubusercontent.com/seminarNotes/studyNotes/main/gif/endeffector-moving.gif
)




### A. 메모
```bash

~/catkin_ws/src/make-package/
├── launch/
│   ├── xxxxx.launch       # Gazebo와 RViz 실행용 launch 파일
├── urdf/
│   ├── yyyyy.urdf.xacro       # 로봇의 URDF 파일 (Xacro 포맷)
├── rviz/
│   ├── zzzzz.rviz             # RViz 설정 파일
├── CMakeLists.txt                       # ROS 빌드 시스템 설정 파일
├── package.xml    

```

|파일|내용|
|--|--|
|launch|Gazebo, Rviz를 실행하고, URDF파일 로드|
|URDF|로봇의 구조, 링크, 조인트, 물리적 특성 정의|
|Rviz|로봇 모델 시각화를 위한 설정|
|CMakeLists.txt|ROS 패키지 빌드 시스템 설정|
|package.xml|ROS 패키지 메타데이터|
