from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, RegisterEventHandler
from launch.conditions import IfCondition
from launch.event_handlers import OnProcessExit
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # Declare arguments
    
    # the declared arguments are used for user to pass customized information from CLI (ros2 launch +declared argument) so that we can change modes
    # if you have multiple launch choice, it's recommended to use IfCondition
    declared_arguments = []
    declared_arguments.append(
        DeclareLaunchArgument(
            "gui",
            default_value="true",
            description="Start RViz2 automatically with this launch file.",
        )
    )

    # Initialize Arguments
    gui = LaunchConfiguration("gui")

    # Get URDF via xacro
    # Command generate a shell command to be executed and dumps the result to your variable
    # in this scenario, robot contains a str of the generated URDF file with all xacro substituted.
    robot_description_content = Command(
        [
            PathJoinSubstitution([FindExecutable(name="xacro")]),
            " ", # do not add extra argument
            PathJoinSubstitution(
                [
                    FindPackageShare("ros2_control_demo_example_1"),
                    "urdf",
                    "rrbot.urdf.xacro",
                ]
            ),
        ]
    )
    # robot description is a dict of str:str, which is for Node to split and leverage when initialize.
    robot_description = {"robot_description": robot_description_content}

    #generate a str of full path.
    robot_controllers = PathJoinSubstitution(
        [
            FindPackageShare("ros2_control_demo_example_1"),
            "config",
            "rrbot_controllers.yaml",
        ]
    )
    rviz_config_file = PathJoinSubstitution(
        [FindPackageShare("ros2_control_demo_description"), "rrbot/rviz", "rrbot.rviz"]
    )

    # in Cmakelist.txt, you specify the executable you create when compile the package.
    #parameters shoud be path to yaml file or dict containing a string of URDF file/
    # output is either log or screen
    # name is the name override, otherwise use 0-1-2-3 to differentiate
    control_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[robot_controllers],
        output="both",
        remappings=[
            ("~/robot_description", "/robot_description"),
        ],
    )
    
    robot_state_pub_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="both",
        parameters=[robot_description],
    )
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="log",
        arguments=["-d", rviz_config_file],
        condition=IfCondition(gui),
    )


    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster", "--controller-manager", "/controller_manager"],
    )

    #this expands to (in equavalence to) CLI command like:
#     ros2 run controller_manager spawner joint_state_broadcaster \
#   --controller-manager /controller_manager \

    #this Run the spawner executable from the controller_manager package.
    # --controller-manager /controller_manager: Tell it that the active controller manager node’s name is /controller_manage
    # After that, Calls /load_controller service on controller_manager to spawn (start) a controller named forward_position_controller.
    # During the compilation process, The infomation in .xml file of every hardware interface and controllers are used to build&registered as a sharelibrary file .so with unique name and type.
    # During the spawning process, the infomation in .yaml file is used by the controller to find the correct .so file and dynamically load the shared library for that controller to initialize.
    # after all these end, the controller converts to configure state(as in a lifecycle node)


    robot_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["forward_position_controller", "--controller-manager", "/controller_manager"],
    )
    

    # Delay rviz start after `joint_state_broadcaster`
    delay_rviz_after_joint_state_broadcaster_spawner = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=joint_state_broadcaster_spawner,
            on_exit=[rviz_node],
        )
    )

    

    nodes = [
        control_node,
        robot_state_pub_node,
        robot_controller_spawner,
        delay_rviz_after_joint_state_broadcaster_spawner,
    ]

# you return a launchDescription with a list of (Nodes + Actions) + list of [DeclareLaunchArgument].
# that's all you need to write a ros launch file!
    return LaunchDescription(declared_arguments + nodes)
