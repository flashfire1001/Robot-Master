# ROS NOTE for source code

> Declaration : This is the first time I really make a dive into the source code of a project. For ROS, the study curve is steep(as it is), so you need to overcome **some** difficulties and trying to figure out how different functions are implemented and how modules interact with their interfaces. Perhaps it's the same story for learning hard things in the future. Just remember, there is always chalenges in your way. Make up your mind , and ... BRAVE IT! 

## Prerequisite:

- The study of ROS control should be based on a good command of programming in Cpp and intermediate knowledge of ROS fundmentals.

- See the docs of ros control to learn about the key concepts(like hardware interface, controller manager, controller ) first.

- Then you should search in ROS wiki/ ROS control doc for lifecycle node to form notion about what is to configure, activate and deactivate the state of a node.  Also, ask AI (I think it's efficient) about the procedure and mechanism of working on a composable node, and focus on how to register a plugin.

## Part1: hardware interface

Some snippets for you to know about: (helps you to understand the code better)

- During the launch state the Controller Manager is first initialise, and it uses the hardware information specified in the URDF .xacro file or .yaml file to construct your Hardware interfaces and controllers.
- The **lifecycle node(controllers, hardware interface they are actually plugin but it's OK to view them like this) exposes hooks**, and the **system orchestrates the transitions** of state through wrappers class(sensor/actuator/system)
- Their transitions (`configure()`, `activate()`) are called **by launch files or CLI**, through controller_manager.
- You should create hardware drivers upon (system_interface, actuator_interface, etc) *_interface.hpp, override methods like read/write.

:dart: Path for you to arrange key your concepts.

1. Start with the **interfaces** (`system_interface.hpp`, `actuator_interface.hpp`, `sensor_interface.hpp`).
2. Then look at the **wrappers** (`system.cpp`, `actuator.cpp`, `sensor.cpp`).
3. Study **component.cpp** to see how lifecycle callbacks are dispatched.
4. Finally, review **handle.hpp** to understand how controllers and hardware actually share data.

### Core Interfaces: `X_interface.hpp`

These are the **abstract classes** you implement in your hardware driver plugins.  
They define the contract between your hardware and the `ros2_control` framework.

---

#### `system_interface.hpp`

- Used for **multi-joint devices** (e.g., arms, mobile robots).
- Inherits from `LifecycleNodeInterface`.
- You must **override** lifecycle and I/O methods.

Key points:

- `on_init(const HardwareInfo & info)`   YOU SHOULD WRITE THIS YOURSELF
  - Called when `configure()` is triggered.  
  - Use `info` (parsed from URDF/YAML) to set up your joints, params.  
  - Return `OK` or `ERROR`.
- `read(const rclcpp::Time & time, const rclcpp::Duration & period)`   YOU SHOULD WRITE THIS YOURSELF
  - Fill joint **state handles** (position, velocity, effort) from hardware.  
  - Called every control loop.
- `write(const rclcpp::Time & time, const rclcpp::Duration & period)`   YOU SHOULD WRITE THIS YOURSELF
  - Write commands from **command handles** to the hardware.
- `export_state_interfaces()`  
  - Declared in `hardware_interface::SystemInterface` / `ActuatorInterface` / `SensorInterface`.  
  - You must return a vector of `StateInterface` objects.  
  - Each `StateInterface` wraps a reference to your internal variables (e.g., joint_position).  
  - Controllers use these to **read states**.

```cpp

//example code:
//in your driver:
class MyMotorDriver : public ActuatorInterface {
private:
    double joint_position_;   // radians
    double joint_velocity_;   // rad/s
    double joint_effort_;     // Nm
public:
    return_type read(const rclcpp::Time & time, const rclcpp::Duration & period) override {
        int32_t ticks = motor_.read_encoder();
        joint_position_ = ticks * TICK_TO_RAD;        // raw -> radians
        joint_velocity_ = (joint_position_ - prev_pos_) / period.seconds();
        joint_effort_ = motor_.read_current() * CURRENT_TO_TORQUE;
        prev_pos_ = joint_position_;
        return return_type::OK;
    }
};
//then define
std::vector<hardware_interface::StateInterface> MyMotorDriver::export_state_interfaces() {
    return {
        hardware_interface::StateInterface("joint1", "position", &joint_position_),
        hardware_interface::StateInterface("joint1", "velocity", &joint_velocity_),
        hardware_interface::StateInterface("joint1", "effort",   &joint_effort_)
    };
}
```

- `export_command_interfaces()`  
  - Similar, but returns `CommandInterface` objects.  
  - Exposes memory locations for commands (e.g., joint_position_command).  
  - Controllers write into these.
- `perform_command_mode_switch(const std::vector<CommandInterface> & start, const std::vector<CommandInterface> & stop)`  
  - Optional hook.  
  - Lets you enable/disable specific command modes (e.g., switch from `position` to `velocity` control).  
  - Return `OK` or `ERROR`.
- `prepare_command_mode_switch()`  
  - Called before `perform_command_mode_switch()`.  
  - Lets you validate if the mode switch is safe.

Notes:

- **info_** : A **configuration object**, filled at startup by parsing your URDF / ros2_control YAML, contains:
  - look up hardware_info.hpp yourself! complex Hierarchy, too hard to explain (ask AI if you want to make this clear) 
  - what is state interface ? [see official api docs](https://control.ros.org/humble/doc/api/classhardware__interface_1_1StateInterface.html)

- lifecycle_state_ :  a struct of 2 parts

  - **State id** (`impl_->get_state().id()`) is used for lifecycle **checks**.  

  - **State name** (`impl_->get_state().label()`) is used for **logs/reports**.  

- You never call these methods directly; `Controller Manager` and wrappers (`system.cpp`) invoke them.

------

### Framework Wrappers

These are the lifecycle-aware **wrappers** that delegate to your implementation:

- Access your real - implementation by a unique pointer **impl_**

- **`system.cpp,actuator.cpp`** (you already looked at)
  
   - Implements `System::read()`, `System::write()` 
   
   - Implements `System::activate()` 
   
   - Implements `export_state_interfaces` , `export_command_interface` , `prepare_command_mode_switch` 
   - These methods from wrapper class first do lifecycle state check through the state id, call the function of impl_ with simply the same/similar name (`system::read()` - `impl_->read()`, `system::shutdown()` - `impl_->on_shutdown()`) , and use the return from these callback function (success/error/fail) to generate respective return.
   
- **`sensor.cpp`**
   Same story but only `read()` is relevant.

These three show the **pattern** of lifecycle → delegate to `impl_`.

------

### Hardware Abstractions and controller communication

- `resouce_manager.hpp/cpp` :

  I haven't probed into the cpp file yet. Skim the header file + chat with AI , I got :

  **Purpose:** gatekeeper

  - Keeps track of **claimed hardware resources** (joints, sensors, actuators) or the **Ownership** 
  - grants the handle to be exchange, with is the crucial data the controller and hardware shares.
  - Ensures that **two controllers don’t write to the same joint simultaneously**.(afety depend on it.)
  - Maps controller requests to hardware interfaces(Controllers query this to know which joints they can command.)

- **`handle.hpp`**
   Defines `CommandInterface` and `StateInterface` → how controllers access joint commands/states.
   Super important: this is how your driver exposes memory to controllers.

   The interface contains 3 parts prefix_name and interface_name and value_ptr , which means "what is the resource(joint/engine motor)" , "what this interface conveys position, velocity" , "the is the current value" respectively.
   
- **`loaned_state_interface.hpp` / `loaned_command_interface.hpp`**
   RAII wrappers for safe access to handles.(they are just another wrapper that contains alias of handles)
   
   - `Loaned*Interface` adds **RAII safety**: a controller temporarily “borrows” memory, ensuring no other controller can access it at the same time.
   - You have full understanding only when you know how Controller manager orchestrate which controller can access which interfaces, how resource manager check and grant the communication. That 's hardware but core of ROS design. (Well, I haven't went deep into it.)
   
- **`hardware_info.hpp`** (In a word, a netted struct)
   Holds URDF/YAML-parsed metadata (names, joints, params).
   You use this in `on_configure`.

------

这都是理论的内容, 看完后试着根据[official guidance](https://control.ros.org/humble/doc/ros2_control/hardware_interface/doc/writing_new_hardware_component.html?utm_source=chatgpt.com) 写一个hardware interface.

## Hardware Control Flow summary

### **Step 1: Controller declares claimed resources**

- Each controller has a **list of resources it wants to control**, e.g., `joint1/position`.
- When the controller is loaded, the **ControllerManager** checks if these resources are available.

------

### **Step 2: ResourceManager tracks ownership**

- `ResourceManager` keeps a **map of resource → claiming controller**.
- When a controller is activated, it **claims the resource**:

```
resource_manager.claim(joint_name, controller_name)
```

- If the resource is already claimed by another active controller, the request fails.
- This guarantees **only one controller can write to a hardware handle at a time**.

------

### **Step 3: Handles connect the controller to the hardware**

- Once the claim is successful, the controller is given **LoanedCommandInterfaces** (or **LoanedStateInterfaces**) that point to the driver’s memory.
- Controller writes into the command handle → later `HardwareInterface::write()` sends it to the actual hardware.

------

A visual:

```text
ControllerManager → Controller requests resource
      │
      ▼
ResourceManager checks ownership
      │
      ├─ if free → grants handle (LoanedCommandInterface)
      └─ if claimed → blocks/throws error
      │
      ▼
Controller can now safely write to the handle
      │
      ▼
HardwareInterface receives command via handle
      │
      ▼
Update with Read or Write()  →  Hardware (motor/joint) moves
```

## Part2 : Controllers and Controller manager

### 1. Controllers

this is from chatgpt:

 `controller_interface_base.hpp`

- **Purpose**: Serves as the foundational base class for all controllers in the `controller_interface` package. It provides essential lifecycle management and interface management functionalities.

- **Key Points**:
  
  - it has a member of a `shared_ptr` to a lifecycle node, and many function , including the management of its lifecycle, takes the advantage of this **node_** member.
  
  - defines the virtual functions that you must override:
  
    - `command_interface_configuration()`
    - `state_interface_configuration()`
    - `update()`
    - `on_init()` 
  
  - issue about "`chainable`" -> your based class `ControllerInterface` / `ChainableControllerInterface` have already helps you set them
  
  - As it works as a lifecycle node, you are encouraged to also implement these functions:
  
    - `on_configure`
    - `on_activate`
    - `on_deactivate`
    - `on_cleanup`
    - `on_error`
    - `on_shutdown`
  
    You don't need to care about how these function is called, there are the callback functions of the `configure, activate, deactivate` of the lifecycle node it uses. This is accomplished through:
  
    ```cpp
      node_->register_on_cleanup(
        std::bind(&ControllerInterfaceBase::on_cleanup, this, std::placeholders::_1));
    
    ```
  
  - `ControllerInterfaceBase::assign_interfaces`: Crucial!
  
    This function securely **transfers ownership** of the Command and State Interfaces from the `ControllerManager` to your specific controller instance. After this function runs, your controller has everything it needs to read sensor data and write commands during every control cycle.
  
    You will understand if you know the whole process: 
  
    1. **Preparation:** The `ControllerManager` first **requests** the required interfaces (e.g., "position commands for joint 1" and "position states for joint 1") from the **Resource Manager** (which knows where the hardware is).
    2. **Loan:** The Resource Manager gathers these interfaces(in a data structure which specified by `hardware_interface/include/handle.hpp`) and **loans** them to the `ControllerManager` (Under the hood, it loans by adding just another alias& wrapper)
    3. **Assignment:** The `ControllerManager` immediately calls your controller's `assign_interfaces` method, passing the loaned interfaces.(use `std::forward` to quickly transfer the loaned interfaces, which is transmitted as **Rvalue** && )
    4. **Usage:** Now, in every subsequent control cycle, when the `ControllerManager` calls your controller's `update()` method, the controller uses those permanently stored interfaces (`this->command_interfaces_` and `this->state_interfaces_`) to perform its calculations.

`chainable_controller_interface.hpp`

- **Purpose**: Extends `ControllerInterfaceBase` to support controller chaining, allowing the output of one controller to serve as the input for another. This is particularly useful in modular control architectures.
- **Key Points**:
  - **Chained Mode**: Introduces the concept of "chained mode," where the controller disables external interfaces to prevent concurrent input commands.
  - **Exporting Reference Interfaces**: Provides methods like `export_reference_interfaces()` to expose command interfaces for chaining, allowing one controller's output to serve as another's input.
  - **Mode Switching**: Includes lifecycle methods specific to chaining, such as `on_set_chained_mode()` and `is_in_chained_mode()`, to toggle between standalone operation and chained operation.

### 2. Controller Manager Control Loop Action

The Controller Manager performs a standard three-step process in each iteration of its main control loop: **Read, Update, and Write**.This cycle ensures a tightly coordinated, periodic execution of the control logic.

| Step          | Action                          | Description                                                  |
| ------------- | ------------------------------- | ------------------------------------------------------------ |
| **1. Read**   | **Hardware → Resource Manager** | The Controller Manager delegates the call to the **Resource Manager** (RM). The RM calls the `read()` method on all active hardware interfaces (e.g., robot drivers) to **get the latest state data (position, velocity, effort).** |
| **2. Update** | **Controller Logic**            | The Controller Manager calls the `update()` method on all **active controllers**. The **controllers read the latest state data from the RM**, compute new control commands based on their logic (e.g., PID), and **write those commands to the command interfaces.** |
| **3. Write**  | **Resource Manager → Hardware** | The Controller Manager delegates the call to the **Resource Manager**. The RM collects the new **commands** from the command interfaces and calls the `write()` method **on all active hardware interfaces to send the commands to the physical robot or simulator.** |

## Part3 : Source Code Reading Guide for Controller manager (Advanced)

### Sequence and Focus Point

| Step                        | Focus Area                                           | Code Files to Refer To                                       | Integral Understanding                                       |
| --------------------------- | ---------------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| **1. Entry Point**          | **Where the CM starts and the loop is initiated.**   | **`controller_manager/src/ros2_control_node.cpp`** This file is the main executable that you launch (or that a launch file calls) | Understand how the main `ControllerManager` object is instantiated and passes it to the **ControllerManagerExecution** thread. This thread is where the real work happens. |
| **2. Control Loop**         | **The `Read-Update-Write` sequence implementation.** | **`controller_manager/include/controller_manager/controller_manager.hpp`** (The `update()` function header)  **`controller_manager/src/controller_manager_execution.cpp`** (The actual loop) | Trace the three core functions (`read()`, `update()`, `write()`) and see how they are called sequentially and periodically. This is the heart of the CM. |
| **3. CM Core Logic**        | **The central class and its key responsibilities.**  | **`controller_manager/include/controller_manager/controller_manager.hpp`** **`controller_manager/src/controller_manager.cpp`** | Focus on the constructor (how it sets up **ROS 2 Services**), the core `update()` implementation (how it iterates over active controllers), and the **lifecycle management** functions like `load_controller()` and `switch_controller()`. |
| **4. Hardware Link**        | **How the CM connects to the hardware.**             | **`resource_manager/include/resource_manager/resource_manager.hpp`** **`resource_manager/src/resource_manager.cpp`** | The CM holds a `resource_manager_` object. Trace how the CM's `read()` and `write()` calls are delegated to the **Resource Manager (RM)**. The RM handles the list of actual hardware plugins. |
| **5. Controller Interface** | **The contract between the CM and any Controller.**  | **`controller_interface/controller_interface.hpp`**          | Look at the **`ControllerInterfaceBase`** class. Focus on the virtual methods that the CM calls: `on_init()`, `on_configure()`, `on_activate()`, `update()`, etc. This defines what any controller *must* do. |

### Key Concepts to Master

- **Real-Time Context:** Notice the use of **`rclcpp::Time`** and **`rclcpp::Duration`** in the `read()`, `update()`, and `write()` function signatures. These are crucial for timing and determinism in the real-time loop.
- **ROS 2 Lifecycle:** The CM manages controllers as **Lifecycle Nodes**. Understanding the **`on_configure`**, **`on_activate`**, **`on_deactivate`**, and **`on_cleanup`** transitions is vital for understanding `load_controller` and `switch_controller` logic.
- **Resource Conflicts:** Pay attention to how the `switch_controller` function checks for **resource (interface) conflicts** before activating a new controller to ensure two active controllers don't try to command the same hardware interface simultaneously.

P. S :Their are also some python files that defines the service API for efficiently dealing with Controller manager and controller&hardware it orchestrates. To be more specific, when you are using the ROS CLI or writing python launch file scripts, you are actually leveraging these exposed API! That's a new layer !

