# Mechianism of ROS2_2: how services work under the hood

------

### Recap: Topics in ROS 2

- Topics are **asynchronous**, one-way message streams.
- Publishers send messages.
- Subscribers receive messages.
- No guaranteed response or acknowledgement.
- Use case: continuous data flow like sensor data, robot status.

------

### What Are Services?

- Services provide **synchronous**, two-way communication.
- A **client** sends a **request** to a **server**.
- The **server** processes the request and sends back a **response**.
- Use case: on-demand computations like “add these two numbers” or “move to this position.”

------

### Differences Between Topics and Services

| Feature            | Topics                        | Services                              |
| ------------------ | ----------------------------- | ------------------------------------- |
| Communication Type | One-way, asynchronous         | Two-way, synchronous                  |
| Data Flow          | Continuous stream of messages | Single request-response pair          |
| Use Case           | Sensors, telemetry, logs      | Remote procedure calls                |
| Blocking           | No                            | Client may block waiting for response |

------

### How Services Work Step-by-Step

Let's say you have a service that adds two numbers:

------

### 1. **Service Definition (`.srv` file)** : meta data for clarifying the data structure.

```srv
int64 a
int64 b
---
int64 sum
```

- Client sends `a` and `b` (request).
- Server returns `sum` (response).

------

### 2. **Generating Code**

From the `.srv` file, ROS 2 auto-generates:

- Request and response message classes/types.
- Serialization/deserialization functions for these messages.

This means the client and server know exactly what data structure to expect.

------

### 3. **How Communication Works Under the Hood (DDS based)**

#### a. Topics Behind the Scenes

- Although a service looks like a request/response, ROS 2 uses DDS topics internally.
- **Two topics** are created per service:
  - **Request topic**: client publishes requests, server subscribes.
  - **Response topic**: server publishes responses, client subscribes.

#### b. Correlation ID

- Each request message is tagged with a **unique correlation ID**.
- This ID helps the client match the correct response to the request it sent.

------

### 4. **Client Behavior**

- The client publishes a request message on the **request topic**.
- Then it waits (blocks or asynchronously) for a response message on the **response topic** with the matching correlation ID.

------

### 5. **Server Behavior**

- The server subscribes to the **request topic**.
- When a request arrives, it runs the callback function you provide.
- It processes the request and publishes the response on the **response topic**, tagging it with the same correlation ID.

------

### 6. **Synchronization**

- The client receives the response and unblocks, getting the data from the server.
- This is how a **remote procedure call (RPC)** happens synchronously in ROS 2.

------

### Visual Diagram (Simplified)

```
Client                     Server
  | -- request (a,b) --> [request topic]
  |                      (subscribed by server)
  |                      Server receives request
  |                      Server processes request
  | <-- response (sum) -- [response topic]
  |                      (subscribed by client)
  Client receives response
```

------

### 7. **Why Not Use Just One Topic?**

- Separating requests and responses into different topics keeps things organized.
- DDS is pub/sub oriented, so ROS 2 uses this two-topic trick to simulate synchronous RPC.

------

### 8. **Programming Perspective**

- You write a **service server** node that:
  - Advertises the service.(send response)
  - Implements a callback that receives the request and returns a response.
  - subscribe to the request topic
- You write a **service client** node that:
  - Sends requests.
  - subscribe to the response topic and wait for it (blocking or async).

------

### Example in C++ (brief snippet):

```cpp
// Server
auto service = node->create_service<AddTwoInts>(
  "add_two_ints",
  [](const std::shared_ptr<AddTwoInts::Request> request,
     std::shared_ptr<AddTwoInts::Response> response) {
       response->sum = request->a + request->b;
  });

// Client
auto client = node->create_client<AddTwoInts>("add_two_ints");
auto request = std::make_shared<AddTwoInts::Request>();
request->a = 5;
request->b = 3;
auto result = client->async_send_request(request);
```

------

### Summary

- **Services** are synchronous request-response pairs.
- Built on DDS topics for request and response.
- Use unique IDs to match requests and responses.
- Enable remote procedure call -like communication.
- Complement the asynchronous topic system.

