# config vscode for ros2

Here is a detailed, step-by-step guide on how to configure VS Code for ROS 2, focusing on a beginner-friendly approach that solves common issues like incorrect syntax highlighting for both C++ and Python.

------



### Step 1: Install Necessary Extensions 🧩



First, you need to install the essential VS Code extensions that provide the core functionality for ROS 2 development.

1. Open VS Code and navigate to the **Extensions** view by clicking the icon on the left sidebar or by pressing `Ctrl+Shift+X`.
2. Search for and install the following extensions:
   - **Python** (by Microsoft): Provides fundamental Python language support.
   - **Pylance** (by Microsoft): A powerful language server that provides IntelliSense, code completion, and type checking for Python. It is a dependency of the Python extension.
   - **C/C++** (by Microsoft): The same as the Python extension, but for C++. This provides IntelliSense, debugging, and code Browse.
   - **ROS** (by Microsoft): The official ROS extension for VS Code. It provides integrated tools for creating packages, running ROS commands, and managing your workspace.

------



### Step 2: Launch VS Code with a Sourced Environment 🚀



This is the **most crucial step** and a frequent point of failure for beginners. VS Code must be launched from a terminal where your ROS 2 environment is already "sourced." This ensures that the editor and its integrated terminal know where to find all the necessary ROS 2 files and commands.

1. Open a new terminal window (e.g., GNOME Terminal).

2. **Source your ROS 2 environment.** Replace `humble` with your ROS distribution (e.g., `jazzy`, `iron`).

   ```
   source /opt/ros/humble/setup.bash
   ```

3. **Source your workspace.** Navigate to the root of your ROS 2 workspace (e.g., `~/ros2_ws`) and source its setup file. This is essential for VS Code to find your custom packages.

   ```
   cd ~/ros2_ws
   source install/setup.bash
   ```

4. **Launch VS Code from this terminal.**

   ```
   code .
   ```

------



### Step 3: Configure C++ IntelliSense ⚙️



This step resolves the red squiggly lines for C++ code by telling the C++ extension where to find the ROS headers.

1. In VS Code, open the Command Palette (`Ctrl+Shift+P`).
2. Search for and select **"C/C++: Edit Configurations (UI)"**. This will open a new window to configure your C++ properties.
3. In the **"Include path"** section, add the following paths. These tell the IntelliSense engine to look in your ROS 2 installation and your workspace's install directory.
   - `/opt/ros/humble/include/**` (replace `humble` with your distro)
   - `${workspaceFolder}/install/*/include/**`
   - `${workspaceFolder}/src/*/include/**`

Alternatively, you can manually edit the `.vscode/c_cpp_properties.json` file in your workspace and add these paths to the `includePath` array.

------



### Step 4: Configure Python IntelliSense 🐍



This step fixes the "unresolved import" errors for Python by configuring the `python.analysis.extraPaths` setting.

1. Go to **File > Preferences > Settings** (`Ctrl+,`).
2. In the search bar, type `python.analysis.extraPaths`.
3. Click the "Add Item" button and add the following paths to the list. This tells the Pylance language server to search for modules in your ROS 2 install directories.
   - `/opt/ros/humble/lib/python3.10/site-packages` (replace `humble` and `3.10` with your distro and Python version)
   - `${workspaceFolder}/install/lib/python3.10/site-packages` (replace `3.10` with your Python version)

It's often easier to edit the `settings.json` file directly. You can find this by clicking the `{}` icon in the top right of the settings window.

```json
{
    "python.analysis.extraPaths": [
        "/opt/ros/humble/lib/python3.10/site-packages",
        "${workspaceFolder}/install/lib/python3.10/site-packages"
    ]
}
```

------



### Step 5: Build and Use the Integrated Terminal ✅



Now that everything is configured, you'll need to build your workspace to generate the files that VS Code needs.

1. Open the **integrated terminal** in VS Code (`Ctrl+``). Because you launched VS Code from a sourced terminal, this terminal should already have the correct ROS 2 environment. You can verify by running `ros2`or`colcon`.

2. **Build your workspace** to compile C++ code and make your Python packages discoverable.

   ```
   colcon build --symlink-install
   ```

   The `--symlink-install` flag is very useful for Python packages, as it creates symbolic links to your source files. This means you can edit your Python code and see the changes immediately without needing to rebuild.

3. **Source your workspace again** in the integrated terminal to make your newly built packages available.

   ```bash
   source install/setup.bash
   ```

4. You can now use the integrated terminal to run your nodes (e.g., `ros2 run my_pkg my_node`) or launch files (`ros2 launch my_pkg my_launch_file.py`), and VS Code will provide accurate IntelliSense and syntax highlighting.



> correctly configuring the IntelliSense paths.

------



### The Fix: Edit the `c_cpp_properties.json` file 🛠️

The solution is to tell the VS Code C/C++ extension exactly where to look for the ROS 2 header files. This is done by editing the configuration file for the IntelliSense engine.

1. **Open the Command Palette** in VS Code by pressing `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac).

2. Search for and select **"C/C++: Edit Configurations (UI)"**. This will open a new window with a user-friendly interface for the configuration file.

3. In the "Include path" section, you need to add two crucial paths:

   - The path to your ROS 2 installation's headers:

     /opt/ros/humble/include/** (Replace humble with your specific ROS 2 distribution, like jazzy or iron.)

   - The path to your workspace's built headers:

     ${workspaceFolder}/install/*/include/**

Alternatively, you can switch to the JSON view by clicking on the `settings.json` icon in the top right of the configurations window and manually add the paths to the `includePath` array.



```json
{
    "configurations": [
        {
            "name": "ROS",
            "includePath": [
                "${workspaceFolder}/**",
                "/opt/ros/humble/include/**",
                "${workspaceFolder}/install/*/include/**"
            ],
            "defines": [],
            "compilerPath": "/usr/bin/gcc",
            "cStandard": "c17",
            "cppStandard": "c++17",
            "intelliSenseMode": "linux-gcc-x64"
        }
    ],
    "version": 4
}
```

After you save this configuration, VS Code will reload the IntelliSense engine, and the errors for `#include "rclcpp/rclcpp.hpp"` and `#include "std_msgs/msg/string.hpp"` should disappear.