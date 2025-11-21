# plan for learning ROS2

the plan for learning humble version of ROS:

1. the key concepts: what is parameter, node, topic and service in ros
2. the code structure of a program based on ROS
3. the file structure and how to build/test/record_log in practice
4. what is ros2 control (extension) ; it's architecture 
5. the code structure of a program relating to ros2 - control (hardware)

> for practice and reinforcement:
>
> - do the task in tutorials
> - learn from some demo
> - examine the META -repository source code and ask when confused
> - do the task assigned by your team.

Specifically:

### Beginner level

- [x] study the the key concepts: what is parameter, node, topic and service in ros
- [ ] note down the key ideas and make a personal lecturenotes for it.
- [ ] learn how to build pkgs and create workspaces / packages
- [ ] note down the key ideas and make a personal lecturenotes for it.
- [ ] learn what publisher/subscriber is like and how to write in Cpp and python
- [ ] note down the key ideas and make a personal lecturenotes for it.
- [ ] learn what service and client is like and how to write in Cpp and python
- [ ] note down the key ideas and make a personal lecturenotes for it.
- [ ] learn how to create custom msg and srv files  + implement custom interface
- [ ] note down the key ideas and make a personal lecturenotes for it.
- [ ] learn how to use parameters in a class (C++ and python)
- [ ] note down the key ideas and make a personal lecturenotes for it.
- [ ] use ros2doctor as well as CLI tools to debug 
- [ ] note down the key ideas and make a personal lecturenotes for it.

### intermediate level

(ask and check where to end)

(ask and check how to learn ROS2-control)

The core of ros2-control is the controller-manager node: with multiple plugin; this node controls sensors and motors with controllers' goal (internally communicate using system interface with command and state attribute) (就好比一堆大脑负责控制躯干的部分运动神经元+感觉神经元)

The more complex work (就好比大脑中负责复杂的体温平衡语言视觉识别逻辑思索的部分)使用各种不同的node; 使用action/service/topic 进行通信. 机制是进程间通信, DDS.

学习the architecture of ros2-control unit. the mechanism and code structure of key parts: controllers, controller-manager, resource manager, and hardware component. how the overlay source the data from the underlay with a set of unified interface.

how to have the node controller-manager interacting with other node.

how the whole program is launched (set up, instantiate and work)

### demos for ROS2

