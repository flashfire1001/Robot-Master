# ROS2 Note: Basic Concepts & CLI Commands

### node

A node in ROS is responsible for a single, modular purpose, e.g. controlling the wheel motors or publishing the sensor data from a laser range-finder. Each node can send and receive data from other nodes via topics, services, actions, or parameters.

A full robotic system is comprised of many nodes working in concert. In ROS 2, a single executable (C++ program, Python program, etc.) can contain one or more nodes.



![../../../_images/Nodes-TopicandService.gif](https://docs.ros.org/en/humble/_images/Nodes-TopicandService.gif)

> the CLI command concerning with node

```bash
ros2 node list
ros2 run <package_name> <executable_name>
# use the args to remapping 
ros2 run turtlesim turtlesim_node --ros-args --remap __node:=my_turtle
ros2 node info <node_name> 
# returns its identity: as subscribers publishers and service (servers and clients)

```

### topic

Topics are one of the main ways in which data is moved between nodes and therefore between different parts of the system. feature: continual, constantly publish and subscribe

> CLI commands

```bash
1.# check with rqt GUI tools
rqt_graph
2.
ros2 topic list 
-t : returns the type of the topic structure/class object
3.
ros2 topic echo <topic_name> # user的监听
4.
ros2 topic info <topic_name> #eg:
Type: geometry_msgs/msg/Twist
Publisher count: 1
Subscription count: 2
5.
ros2 interface show <msg_type> #show the metadata/interface of the topic
#eg. This expresses velocity in free space broken into its linear and angular parts.
    Vector3  linear
            float64 x
            float64 y
            float64 z
    Vector3  angular
            float64 x
            float64 y
            float64 z
 6.manually pub a message use a topic
 ros2 topic pub <topic_name> <msg_type> '<args>'
 7.view the rate at which the data is published
 ros2 topic hz /turtle1/pose
#ros2 topic pub --rate 1 this can set the publishing rate
8. find a topic using its type
ros2 topic find <topic_type>
```

### service

Services are another method of communication for nodes in the ROS graph. **Services are based on a call-and-response model versus the publisher-subscriber model of topics.** While topics allow nodes to subscribe to data streams and get continual updates, services only provide data when they are specifically called by a client.

> CLI commands

```bash
1.
ros2 service list 
-t : returns the type of the topic structure/class object
2. find the service type
ros2 service type <service_name>
3.find a service using its type
ros2 service find <type_name>
4.
use the parameter service to check the parameter metadata/interface
so that you can better set the data
5.
ros2 interface show turtlesim/srv/Spawn
float32 x
float32 y
float32 theta
string name # Optional.  A unique name will be created and returned if this is empty
---
string name

 6.manually call a message through service method
 ros2 service call <service_name> <service_type> <arguments>

```



### Parameter

A parameter is a configuration value of a node. You can think of parameters as node settings. A node can store parameters as integers, floats, booleans, strings, and lists. In ROS 2, each node maintains its own parameters. 

```bash
ros2 param list
#Every node has the parameter use_sim_time; it’s not unique to turtlesim.

# to access the current value of a parameter
ros2 param get <node_name> <parameter_name>

eg.ros2 param get /turtlesim background_g
Integer value is: 86

#To change a parameter’s value at runtime, use the command:
ros2 param set <node_name> <parameter_name> <value>

#view all of a node’s current parameter values by using the command:
ros2 param dump <node_name> 
ros2 param dump /turtlesim > turtlesim.yaml

# load params from a file to a currentlly runninf node
ros2 param load <node_name> <parameter_file>
#load on start up
ros2 run <package_name> <executable_name> --ros-args --params-file <file_name>
```

### actions

![../../../_images/Action-SingleActionClient.gif](https://docs.ros.org/en/humble/_images/Action-SingleActionClient.gif)

```text
  In ros2 node info ,
  we can see the action info:
  
  Action Servers:
    /turtle1/rotate_absolute: turtlesim/action/RotateAbsolute
  Action Clients:
```

```
ros2 action list -t list all the action with type

ros2 action info (similar to topic)
eg:
ros2 action info /turtle1/rotate_absolute
Action: /turtle1/rotate_absolute
Action clients: 1
    /teleop_turtle
Action servers: 1
    /turtlesim

eg:
ros2 interface show turtlesim/action/RotateAbsolute
# The desired heading in radians
float32 theta
---
# The angular displacement in radians to the starting position
float32 delta
---
# The remaining rotation in radians
float32 remaining
```



Now let’s send an action goal from the command line with the following syntax:

```
$ ros2 action send_goal <action_name> <action_type> <values> --feedback
```

`<values>` need to be in YAML format.

returns

```bash
sending goals

Feedback: updates in the process

Result
```

