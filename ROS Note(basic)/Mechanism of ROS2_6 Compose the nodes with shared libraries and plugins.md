# Mechanism of ROS2_6: Compose the nodes with shared libraries and plugins
In ROS 2, you can run multiple nodes in a single process using the **composition** mechanism.
 The idea is: instead of starting each node as a separate executable, you **load node classes into one shared process** (like plugins) so they can communicate more efficiently and share memory.

------

## 1. Why do this?

- **Lower latency** — intra-process communication (zero-copy or reduced copies).
- **Lower overhead** — fewer OS processes, fewer context switches.
- **Easier lifecycle management** — start/stop nodes programmatically.

------

## 2. Key concepts

| Concept                 | Meaning                                                      |
| ----------------------- | ------------------------------------------------------------ |
| **Composable Node**     | A ROS 2 node written so it can be loaded dynamically into another process. |
| **Component**           | The implementation of a composable node, registered as a plugin with `rclcpp_components`. |
| **Component Container** | The process (executable) that loads and runs one or more components. |

------

## 3. Steps to compose multiple nodes

### Step 1: Create composable node classes

Instead of a `main()`, you make a class inheriting `rclcpp::Node` and export it as a plugin.

**Example: `talker_component.cpp`**

```cpp
#include <rclcpp/rclcpp.hpp>
#include <std_msgs/msg/string.hpp>
#include "rclcpp_components/register_node_macro.hpp"

class Talker : public rclcpp::Node {
public:
  explicit Talker(const rclcpp::NodeOptions & options)
  : Node("talker", options) {
    publisher_ = this->create_publisher<std_msgs::msg::String>("chatter", 10);
    timer_ = this->create_wall_timer(
      std::chrono::seconds(1),
      [this]() {
        auto msg = std_msgs::msg::String();
        msg.data = "Hello";
        publisher_->publish(msg);
      });
  }

private:
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
  rclcpp::TimerBase::SharedPtr timer_;
};

RCLCPP_COMPONENTS_REGISTER_NODE(Talker)
```

**CMakeLists.txt snippet**

```cmake
find_package(rclcpp REQUIRED)
find_package(rclcpp_components REQUIRED)
find_package(std_msgs REQUIRED)

add_library(talker_component SHARED talker_component.cpp)
ament_target_dependencies(talker_component rclcpp rclcpp_components std_msgs)
rclcpp_components_register_nodes(talker_component "Talker")
```

------

### Step 2: Create a container to load them

You can use:

- **Prebuilt container**: `ros2 run rclcpp_components component_container`
- **Custom container executable** (lets you set parameters, QoS, etc.)

**Example: `my_container.cpp`**

```cpp
#include <rclcpp/rclcpp.hpp>
#include <rclcpp_components/component_manager.hpp>

int main(int argc, char ** argv) {
  rclcpp::init(argc, argv);
  auto exec = std::make_shared<rclcpp::executors::MultiThreadedExecutor>();
  auto manager = std::make_shared<rclcpp_components::ComponentManager>(exec);
  exec->add_node(manager);
  exec->spin();
  rclcpp::shutdown();
  return 0;
}
```

------

### Step 3: Launch and load multiple nodes

You can load components into the container:

- **From command line**

```bash
# Start container
ros2 run rclcpp_components component_container

# Load multiple components into it
ros2 component load /ComponentManager <package_name> <plugin_name>
ros2 component load /ComponentManager <package_name> <another_plugin>
```

- **From a launch file**

```python
from launch_ros.actions import ComposableNodeContainer, ComposableNode
from launch import LaunchDescription

def generate_launch_description():
    container = ComposableNodeContainer(
        name='my_container',
        namespace='',
        package='rclcpp_components',
        executable='component_container_mt',
        composable_node_descriptions=[
            ComposableNode(
                package='my_pkg',
                plugin='Talker',
                name='talker'),
            ComposableNode(
                package='my_pkg',
                plugin='Listener',
                name='listener')
        ],
        output='screen'
    )

    return LaunchDescription([container])
```

------

### Step 4: Intra-process optimization

When you use composition, enable **intra-process communication**:

```cpp
rclcpp::NodeOptions options;
options.use_intra_process_comms(true);
```

This reduces copies for messages passed between nodes in the same process.

------

✅ **Summary**
 To compose multiple nodes into one process:

1. Write each node as a **component** (no `main()`, inherit `rclcpp::Node`).
2. Build them as **shared libraries** with `rclcpp_components`.
3. Load them into a **container** (prebuilt or custom) via CLI or launch file.
4. Use **intra-process comms** for maximum speed.

### EXTRA POINTS

shared library and plugins about **how code is packaged and loaded into a running process**.

------

## 1. What’s a shared library?

A **shared library** is a file (usually ending in `.so` on Linux) that contains compiled code which **isn’t an executable by itself** — it must be loaded by another program.

Example:

- Executable: `/usr/bin/ls` → you can run it directly.
- Shared library: `/usr/lib/libm.so.6` → can’t run it, but programs can load it to use math functions.

In ROS 2 composition:

- Your **node class** is compiled into a `.so` file.
- The container process loads that `.so` file *while it’s running* — without restarting.

------

## 2. What’s a plugin?

A **plugin** is just a class/function inside a shared library that’s registered in a way that other code can find and use it without knowing its exact type at compile time.

In ROS 2:

- You write a class that inherits from `rclcpp::Node`.

- You register it with a macro:

  ```cpp
  RCLCPP_COMPONENTS_REGISTER_NODE(Talker)
  ```

- This puts your node into a **plugin registry**.

- The container later says: “Load the plugin named `Talker` from package `my_pkg`.”

This uses the **pluginlib** package in ROS 2, which under the hood:

- Opens your `.so` file at runtime (`dlopen` in Linux).
- Finds your class by its registered name.
- Creates an object of it with `new`.

------

## 3. How it all connects

Think of it like **LEGO**:

- **Shared library (.so)** → a LEGO brick you built, stored in a box.
- **Plugin registration** → putting a label on that brick so others know what it is.
- **Container** → a LEGO baseplate that lets you attach bricks at runtime.
- **Launch file** → a plan telling the container which bricks to place and where.

No threads are inherently involved in the plugin system — though once the container runs your node, the executor may use multiple threads if you choose (`component_container_mt`).

------

## 4. Why ROS 2 uses this

- You can run nodes separately (each in their own process).
- Or load multiple into the same process (composition) to avoid serialization overhead.
- Plugins let you pick **which nodes to load** at runtime without recompiling the container.

------

If you want, I can **draw you a diagram** showing how:
 `ComposableNodeContainer → pluginlib → shared library (.so) → your node instance`.

It’ll make the mental picture click instantly.