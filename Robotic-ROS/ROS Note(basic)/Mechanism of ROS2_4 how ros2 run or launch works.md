# Mechanism of ROS2_4: how ros2 run or launch works?

> we use package.xml and setup.cfg/py in python cmakelist.txt in cpp for the build process. It's crucial to learn how the dependency libs/packages are specified(and represented in setup.bash) and how path of relative executables are placed in the install folder under your workspace. This article aims to give you an clear, beginner-friendly guidance to understand the mechanism that make ros2 runs and launch smoothly.

ROS 2 might look magical at first — you type `ros2 run` or `ros2 launch` and things just… start running.
 But behind the scenes, there’s a very precise mechanism that depends on how your package is **built** and **installed**.If you understand how files are placed in your workspace’s `install/` folder, the magic becomes simple logic.

------

## 1️⃣ Declaring a ROS 2 Package

Whether your node is in **Python** or **C++**, you always start with **`package.xml`**.

### `package.xml` — the identity card of your package

- **Defines name, version, description** (human-readable metadata). Be sure to match and make it correct is enough for you.

- **Declares dependencies**:

  - `build_depend`, `exec_depend`, `test_depend`, etc.

  - Example:

    ```xml
    <exec_depend>rclpy</exec_depend>   <!-- runtime dependency -->
    <exec_depend>std_msgs</exec_depend>
    ```

- Used by **`colcon`** to:

  1. Figure out the build order.
  2. Install required system packages (via `rosdep`).
  3. Generate setup scripts that make ROS aware of your package.

**Key point:**
 If your `package.xml` misses a dependency, the build might fail **or** your node will fail at runtime because the library/package is missing.

------

## 2️⃣ Declaring the Build Process

ROS 2 supports different build types:

### For Python nodes — `ament_python` build

- You provide:

  - `setup.py` (build + install instructions)
  - `setup.cfg` (often minimal, telling setuptools where the source is)

- In `setup.py`:

  - **Entry points** → tell ROS 2 what “executables” your package has.

    ```python
    entry_points={
        'console_scripts': [
            'minimal_param_node = python_parameters.minimal_param_node:main',
        ],
    }
    ```

    This creates a **wrapper executable** in `install/lib/<package>/` that calls your Python function.

  - **Data files** → non-Python resources like `launch/` files.

    ```python
    data_files=[
        (os.path.join('share', package_name), ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
    ]
    ```

    Without this, `ros2 launch` won’t find your launch files.

------

###  For C++ nodes — `ament_cmake` build

we already know that, ROS2 harness the advantage of a cmake plugin -- ament, which defines a lots of macro of cmake exclusively for ROS.

- You provide:

  - `CMakeLists.txt` with build + install rules.

- Example:

  ```cmake
  add_executable(talker src/talker.cpp)
  ament_target_dependencies(talker rclcpp std_msgs)
  
  install(TARGETS talker
    DESTINATION lib/${PROJECT_NAME}
  )
  
  install(DIRECTORY launch
    DESTINATION share/${PROJECT_NAME}
  )
  ```

  - `install(TARGETS ...)` → puts your binary into `install/lib/<package>/`.
  - `install(DIRECTORY launch ...)` → copies launch files into `install/share/<package>/launch/`.

------

## 3️⃣  Building and Installing

When you run:

```bash
colcon build
```

For each package:

1. **Build artifacts** are generated in `build/<package>/`.
2. **Install step** copies them into `install/<package>/` (or directly into `install/` if merged install).
3. The **ament resource index** is updated — a registry telling ROS 2 where your package’s **lib** and **share** folders are.

------

## 4️⃣ Environment Setup (`setup.bash`)

Before you can run anything, you **must**:

```bash
source install/setup.bash
```

This script:

- Updates environment variables:
  - `AMENT_PREFIX_PATH` → where to find installed packages.
  - `PYTHONPATH` → where to import Python modules from.
  - `PATH` → sometimes updated for executables in `bin/`.
  - `LD_LIBRARY_PATH` → where to find C++ shared libraries.
- Registers your package in ROS’s internal index.

Without sourcing, `ros2 run` / `ros2 launch` will say:

```
Package '<name>' not found
```

> chain of responsibility:

If we trace *all the way down*, the flow looks like:

```text
setup.bash
  ↓
local_setup.bash
  ↓
setup.sh   ← finds all prefixes(opt/ros/humble, ws/install/, ...etc)
  ↓
local_setup.sh in each prefix
  ↓
package.sh hooks in share/<package>/hook/
      ↓
      export PATH, LD_LIBRARY_PATH, PYTHONPATH, AMENT_PREFIX_PATH, etc.
```



## 5️⃣  How `ros2 run` Works

When you type:

```bash
ros2 run my_package my_executable
```

ROS 2:

1. Uses the **ament index** to find `install/share/my_package`.
2. From there, finds the **prefix** (`install/<package>`).
3. Looks for `lib/my_package/my_executable` inside that prefix.
4. Spawns that executable as a subprocess.
5. Passes any ROS arguments (`--ros-args`) to it.

📌 **Important:**
 If your binary isn’t installed to `install/<package_name>lib/<package>`, `ros2 run` will never find it.

------

## 6️⃣ How `ros2 launch` Works

When you type:

```bash
ros2 launch my_package my_launch.py
```

ROS 2:

1. Finds your package’s `share` directory.
2. Looks inside `share/my_package/launch/` for `my_launch.py`.
3. Runs it using Python.
4. The launch file returns a `LaunchDescription` — a plan of what nodes to start, with what parameters and remappings.
5. The `launch` system executes those nodes (often via `Node()` actions that internally call the same logic as `ros2 run`).

> In ROS 2’s launch system, your `launch.py` file isn’t run like a normal Python script — **it’s imported and executed by the `ros2 launch` process**, which *calls* your `generate_launch_description()` function for you.
>
> ------
>
> ## Step-by-step of what’s happening
>
> 1. **You run**
>
>    ```bash
>    ros2 launch <package_name> <launch_file>.py
>    ```
>
> 2. **`ros2 launch` command**
>
>    - Is part of the `launch`/`launch_ros` Python framework.
>
>    - It **loads your Python file as a module** (not as a `__main__` script).
>
>    - It looks for a function called:
>
>      ```python
>      generate_launch_description()
>      ```
>
>      This is a *convention* required by the launch system.
>
> 3. **Framework calls your function**
>
>    - The `launch` tool calls:
>
>      ```python
>      ld = generate_launch_description()
>      ```
>
>    - This returns a `LaunchDescription` object containing the actions you defined (Nodes, Loggers, etc.).
>
> 4. **Launch service executes actions**
>
>    - The `LaunchService` takes your `LaunchDescription` and *executes* the actions:
>      - Starts the `Node` processes.
>      - Handles parameters.
>      - Configures output.
>
> ------
>
> ### Why there’s “no execution” in your file
>
> - There’s no `if __name__ == "__main__":` block because **you never run the file directly**.
> - The *launcher* is the main program; your launch file is essentially **a config in Python form**.
>
> ------
>
> ### Analogy
>
> Think of it like a **plugin system**:
>
> - You write a function that returns a set of instructions.
> - ROS 2 is the host program that imports your plugin and runs those instructions.
>
> ------
>
> If you want, I can show you **exactly which part of ROS 2’s `ros2 launch` code imports your file and calls `generate_launch_description()`** — that makes the magic very clear. Would you like me to trace that?

------

## 7️⃣ Putting it All Together — The Flow

```
Source Code (Python/C++)
    │
    ├── package.xml        # Dependencies + metadata
    ├── setup.py / CMakeLists.txt
    │       ├── install targets
    │       └── entry points / binaries
    ├── launch/
    │
colcon build
    │
    ▼
Install Space
    ├── lib/<package>/node_executable
    └── share/<package>/launch/*.launch.py
    │
source install/setup.bash
    │
    ├── AMENT_PREFIX_PATH → points to install space
    ├── PYTHONPATH        → finds Python nodes
    └── PATH/LD_LIBRARY_PATH updates
    │
ros2 run <pkg> <exe>
    │
    └── Finds lib/<pkg>/<exe> and runs it
ros2 launch <pkg> <file>
    │
    └── Finds share/<pkg>/launch/<file> and runs launch system
```

------

## 8️⃣ Quick Debugging Checklist

- error in build process?
  - check dependencies in package.xml

- **Executable missing?**

  - C++: check `install(TARGETS ...)` in CMake.
  - Python: check `entry_points` in `setup.py`.

- **Launch file not found?**

  - Did you install it to `share/<pkg>/launch`?

- **Package not found?**

  - Did you `source install/setup.bash`?

- **Check package visibility:**

  ```bash
  ros2 pkg prefix my_package
  ros2 pkg executables my_package
  ```

------

## 🎯 Key Takeaways

1. **`package.xml`** → tells ROS what your package is and what it needs.
2. **Build file** (`setup.py` or `CMakeLists.txt`) → tells ROS how to build/install it.
3. **Install space layout** is *fixed*:
   - Executables in `lib/<pkg>/`
   - Launch files in `share/<pkg>/launch/`
4. **`setup.bash`** → updates environment so ROS tools can find your package.
5. **`ros2 run`** → finds and runs a single executable.
6. **`ros2 launch`** → runs a launch file that can start multiple nodes.

坦诚的说, 看完这篇文章后, 我自己还是没有彻底搞明白ros的构造...(所以随便看看吧bushi)

哈哈哈哈哈.....