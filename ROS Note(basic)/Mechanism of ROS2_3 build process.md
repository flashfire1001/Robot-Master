# how **colcon**, **CMake**, and **ament** interact in a ROS 2 build?

------

### Quick reminder:

| Tool       | Abstraction Level            | What it manages                                              |
| ---------- | ---------------------------- | ------------------------------------------------------------ |
| **colcon** | **Highest-level build tool** | Manages **whole workspace with multiple packages**; decides build order, calls underlying build tools (usually CMake), handles install, test, and more. |
| **CMake**  | **Build system generator**   | Generates build instructions (like Makefiles) **per package/project** based on high-level configuration. Handles dependency and platform specifics. |
| **make**   | **Low-level build tool**     | Reads generated build instructions (Makefile) and runs compiler commands (gcc/g++) to compile and link source files. |

- **colcon**: Workspace-level build tool that builds multiple packages in the right order.
- **CMake**: Build system generator that creates Makefiles or Ninja files.
- **ament**: ROS 2’s **build system and package management framework**, built on top of CMake.

------

## How colcon controls CMake **through ament**

1. **ament_cmake** is a **CMake extension/package** that adds ROS 2-specific macros, functions, and conventions to your `CMakeLists.txt`.

   - It defines commands like `ament_package()`, `ament_target_dependencies()`, and ROS 2 specific build helpers.
   - This helps your package integrate with ROS 2’s build ecosystem (message generation, interface generation, dependencies, testing, etc.).

2. When you run:

   ```bash
   colcon build
   ```

   - **colcon scans all packages** in your workspace.
   - For each package that uses **ament_cmake** (your typical C++ ROS 2 package), colcon:
     - Calls `cmake` **with special environment variables and arguments** that activate `ament_cmake` tooling.
     - CMake processes your `CMakeLists.txt` which uses `ament_cmake` commands to configure your package correctly.
     - This triggers:
       - ROS 2 interface generation (from `.msg`, `.srv` files).
       - Dependency discovery and setup.
       - Compiler flags, include paths, install rules, tests, etc.

3. After configuring with CMake and `ament_cmake`, colcon:

   - Runs `make` (or Ninja) to actually compile and link the package.
   - Collects build results, logs, and installs built targets.

------

### Visual flow

```
colcon build
    ↓
for each package:
    calls cmake with ament_cmake activated
        ↓
    CMake + ament_cmake read CMakeLists.txt
        ↓
    generate build files + ROS 2 specific code generation
        ↓
    make compiles, links, installs
```

------

### Why use ament?

- It **standardizes ROS 2 package building**.
- Provides macros and helpers specific to ROS 2 needs.
- Simplifies interface generation, dependencies, testing, and installing.
- Makes `colcon` + CMake work smoothly together in ROS 2 projects.

