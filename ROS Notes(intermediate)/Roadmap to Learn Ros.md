# Road map to Learn Ros: A direct, task-oriented approach

>  一个ros速成的明确攻略, 写给像我这样学习需要明确资源指路和方向指导的人.

As a beginner who want to enhance the understanding of ROS and coding skill, the central task should be:

**Learn ROS and write a simple ROS controller.** 

### (i) review basics:

- 此处看官方文档,基本概念解释得很清楚.https://docs.ros.org/en/humble/index.html
- ROS Concepts like topic, node, node with lifecycle, composable node.
- ROS lifecycle official demo(well explained) in github: [url](https://github.com/ros2/demos/tree/humble/lifecycle)
- The ros cli tools usage (reinforce in practice, that more fundamental)
- ros - control: controller, hardware component/controller interface: command/state/reference. manager.
- 学有余力, 建议看tf2, URDF, launch 这样你对ros会有更全面的了解.

### (ii) dive into code!!!

首先你要知道,你面对的是什么:

- project architecture:

  > - `CMakeLists.txt` file that describes how to build the code within the package; `package.xml` file containing meta information about the package
  > - `include/<package_name>` directory containing the public headers for the package
  > - `src` directory containing the source code for the package
  > - bringup 
  > - description 
  > - hardware
  > - `.xml `file

  - dependency (specified by Cmakelist/package.xml...) 这建议你直接问AI. 没有很好的教程和整理
  - folded include/build/src. install

- description file:  urdf, yaml [机器描述文件](https://docs.ros.org/en/humble/Tutorials/Intermediate/URDF/URDF-Main.html) +  launch.py的[启动脚本](https://docs.ros.org/en/humble/How-To-Guides/Launch-file-different-formats.html) (学有余力学一下)

- Code implementation:
  - 建议先看源代码的hpp文件, 熟悉一下各种内部API;不会的问AI , 每个概念是怎么代码实现的
  - 源代码只需要知道基本实现机制. 让你是在不懂的内容可以扫读(没用,不是你在写ROS框架)
  - 学有余力看cpp文件, 你会发现内部有许多service 使得cli和launch file能顺利和controller manager对接; 开始CM是怎么创建各个hardware interface 和 controller的; 每一个control loop 它干了什么: how controller manager orchestrate the controllers and hardwares through resource manager is delicately designed.
  - 然后你就可以看demo了

更新,这部分的具体内容:

时间紧急, 直接看ROS_control的内容, 同时自行把ROS的内容迁移理解(是可行的)

- 具体案例:ROS control 1,2,3(之前学了xacro的可以看看7) 看源代码! 用如下代码安装:

```bash
cd ~/ros_demo_ws/src

git clone -b humble https://github.com/ros-controls/ros2_control_demos.git
cd ~/ros_demo_ws

rm -rf log install build

colcon build --symlink-install --cmake-args -DCMAKE_EXPORT_COMPILE_COMMANDS=ON

# option 2
mkdir -p ~/ros_demo_ws/src
cd ~/ros_demo_ws/src
git clone https://github.com/ros-controls/ros2_control_demos -b humble
# then you can build the repo
cd ~/ros_demo_ws/
. /opt/ros/${ROS_DISTRO}/setup.sh
colcon build --symlink-install --cmake-args -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
ln -sf build/compile_commands.json compile_commands.json
# 在这之后,即直接用launch 命令就可以看到gazebo/rviz simulation的效果了,要source 防止出现package not found.
source ~/ros_demo_ws/install/setup.bash
ros2 launch ros2_control_demo_example_1 view_robot.launch.py
```

- 这几个项目可以当作你的练手项目, 本身简单的逻辑让你很容易diy来熟悉代码运行逻辑.
- 看demo背后的代码(你需要下载controllers 和 demos自己编译); 你可以全部都看(这样可以了解从hardware配置, launch处理到controller撰写的全部内容), 也可以单独只看核心的controller 如何写的. [源码](https://github.com/ros-controls/ros2_controllers/tree/humble)

进一步:

- 官方hardware interface的教程(学习ROS_control设计逻辑和重要的class/member)>
- 看ros/execution/meta_hardware 这里要知道每个class, 结合hardware_interface的源代码
- 看ros/decomposition/gimbal_controller 此处结合control_interface 源代码

学完这一部分,你已经有了尝试自己使用interface写一个controller的基本能力

### (iii) sketch your task: where should you modify?

- 想一想,你需要基于什么修改重写, 你的controlling logic是什么; 想一想, 你用到的hardware interface是什么, 怎么用.

Here is my example, using 

- velocity
- effort (PID -> velocity to effort)

### (iv) Debug and deploy : Anyway, you are near the final success!

本人的debug notes:

-  写一部分, debug 一部分, 这会防止出现复杂的相互依赖的错误.

- 当你写完后, 进入配置环节: 也就是 urdf, yaml机器配置文件(当然, 一般你应该先写好这部分, 再思考控制逻辑) + package.xml 和cmake.list的编译依赖文件 + 自动初始化  launch.py脚本. 这三者对新手很不友好(先说清楚了)
- 看队长写的或者网上的教程, 搞懂urdf和yaml的配置文件的意思,launch脚本的机理.(至于如何build,关于cmakelist 和package.xml请问ai/学长) --- 总之, 这里有别人带着你是最好的, 不然只有AI还是很痛苦的. 不管怎么样, 刚开始都是痛苦的, 慢慢的写过几个项目后你就可以独立地写它了.



### BONUS: some encouragements and counsel

这里是所有代码资源网址:

> 战队的代码:https://github.com/Meta-Team/Meta-ROS/tree/master/decomposition/meta_chassis_controller,  https://github.com/Meta-Team/Meta-ROS/tree/master/decomposition/meta_gimbal_controller,  https://github.com/Meta-Team/Meta-ROS/tree/master/decomposition/meta_shoot_controller 
>
> hardware interface的综述和教程https://control.ros.org/humble/doc/ros2_controllers/doc/writing_new_controller.html ; https://control.ros.org/humble/doc/ros2_control/hardware_interface/doc/hardware_components_userdoc.html
>
> 看demo用到的源码https://github.com/ros-controls/ros2_controllers/tree/humble
>
> 网上比较优秀的教程:https://www.guyuehome.com/

如果你时间空余,正常1个多月把这些做完. 如果你赶时间, 你也大概需要十几天. 总之, 把ROS上手的任务当作你个大一点的mp, 或许会更有挑战的动力和勇气. 不要急, 也不要怕, 坚持做就好.

Remember. new/strange always comes with challenges. Never let them stop you from attempts & progress!

Check Box: help keep you on track!

- [x] review the basic concepts 
- [x] run and check the demo 1,2,3 or more.
- [x] look through the source code as well as demo code.
- [x] look through the [team](https://github.com/Meta-Team/Meta-ROS) code, find their control logic/ sort out a class/method table for you to further refer to as a resource.
- [x] start coding your own controller!
- [x] debug it and work with dependency / other issues
- [ ] finalize your first project(though it's primary) and deploy it! 
- [ ] share it with your friends. They will be proud of you! :joy: