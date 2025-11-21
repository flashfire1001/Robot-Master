# Mechanism of ROS21: Communication of Topics Under the hood.

This article will walk through **how ROS 2 moves data from a publisher to a subscriber** step-by-step.

------

## **1. Nodes and Topics**

- In ROS 2, **nodes** are your programs (`MinimalPublisher`, `MinimalSubscriber`, etc.).
- Nodes communicate via **topics** (named data channels, e.g., `"chatter"`).
- Publishers send messages *to* a topic, subscribers read messages *from* a topic.

------

## **2. The Middleware Layer (DDS)**

ROS 2 doesn’t send messages directly between Python/C++ objects.
 Instead, it uses a **middleware** — specifically DDS (**Data Distribution Service**), which is a peer-to-peer publish/subscribe system.

**DDS is responsible for:**

- Finding **matching** publishers and subscribers.
- Handling **data serialization/deserialization **.
- the data serialization is language independent -- because  Your ROS 2 `.msg` file (e.g., `std_msgs/String.msg`) is automatically converted by `rosidl` into an **IDL (Interface Definition Language)** file, the language-neutral schema defined by OMG standards. 
- Then, ROS 2 adopts DDS’s standard serialization format—**CDR**—which is language and architecture neutral. It respects **alignment rules**, packing the message into bytes. The deserialization is vice versa. 
- **Delivering data** over the network (or locally).
- Managing QoS (reliability, history, etc.).

Think of DDS as the **post office** for ROS 2.

------

## **3. Step-by-Step Communication Flow**

Let’s say you have:

```python
publisher = node.create_publisher(String, "chatter", 10)
subscriber = node.create_subscription(String, "chatter", callback, 10)
```

------

### **A. Discovery Phase (before sending data)**

1. **Node A** (publisher) tells DDS:
   - “I publish to topic `chatter` of type `std_msgs/String`.”
2. **Node B** (subscriber) tells DDS:
   - “I subscribe to topic `chatter` of type `std_msgs/String`.”
3. DDS automatically **matches them** if:
   - Topic names match (`"chatter"`).
   - Message types match (`std_msgs/String`).
   - QoS policies are compatible.

📌 This happens **without** a central server — all DDS participants discover each other.

------

### **B. Publishing a Message**

1. Your Python code calls:

   ```python
   publisher.publish(msg)
   ```

2. The message is:

   - Serialized (converted into bytes).
   - Passed down to DDS.

3. DDS sends the serialized bytes:

   - If subscriber is in the same process → delivered directly in memory.
   - If in another process on the same machine → sent via **shared memory** or loopback network.
   - If on a different machine → sent over **TCP/UDP** (depending on QoS).

------

### **C. Receiving a Message**

1. DDS on subscriber’s side receives the bytes.
2. DDS **deserializes** them back into a `String` object.
3. DDS hands the message to ROS2 ’s callback queue.
4. When you `rclpy.spin(node)`:
   - The callback (`callback(msg)`) is called with the new data.

------

## **4. Visual Diagram**

```
Publisher Node ──[serialize]──▶ DDS ──network/SHM──▶ [deserialize]── Subscriber Node
       |                                                    |
  publish(msg)                                      callback(msg)
  
```

------

> **In Short, when the program start runs, the DDS domain(part of RMW) is initialized, then the subscriber and  publisher are created with a dds ID for them to be matched. When a message is published, the DDS work as a data pipeline: it receive the message and serialize, transmit, deserialize it. After that, the subscriber node is beckoned, which will do its callback function with the message.**

## **5. Key Points**

- No direct Python-to-Python(Cpp) sending — DDS handles everything.
- Publisher and subscriber don’t know each other’s IPs or process IDs — DDS takes care of discovery and delivery.
- QoS settings control **reliability**, **latency**, and **history**.
- The system works across:
  - Same process
  - Different processes on same machine
  - Different machines on a network

------

> DDS is **inside every ROS 2 node process**, and you don’t explicitly call it most of the time.

------

### **How That Happens**

1. When you write:

   ```python
   import rclpy
   rclpy.init()
   ```

   you’re not just setting up some Python lists — you’re actually loading the **RMW (ROS Middleware) layer** for your chosen DDS vendor (e.g., Fast DDS, Cyclone DDS).

2. This RMW layer **creates a DDS participant** in the background:

   - Registers the process as part of the DDS domain.**(multi-cast memory, where nodes introduce themselves to each other)**
   - Sets up networking threads, discovery beacons, QoS configs.
   - This is all “invisible” to you — you never call `dds_init()` yourself.

3. Whenever you do:

   ```python
   self.create_publisher(String, "chatter", 10)
   ```

   it **tells the DDS participant**:

   - “Make a DataWriter for topic `chatter` of type `String`.”
   - DDS then announces it to other participants automatically.

4. DDS handles:

   - **Discovery** (finding other nodes).
   - **Matching** (linking publishers to subscribers).
   - **Data transfer** (serialize, send, receive, deserialize).
   - **Liveliness** monitoring (detecting dead processes).

------

### **Why It’s “Inexplicit”**

- You never import DDS directly (like `import fastdds`).
- You only interact with ROS 2’s public API (`rclpy`, `rclcpp`).
- ROS 2’s RMW implementation calls DDS vendor APIs **under the hood**.
- Each process gets its own DDS runtime **embedded** inside it.

------

**Analogy:**
 It’s like using Python’s `requests` library — you just say `requests.get(url)`, but under the hood it’s opening sockets, managing TLS, and handling HTTP protocol without you ever touching those parts.