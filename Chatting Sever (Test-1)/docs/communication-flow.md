# Network Communication Flow

## Overview
The communication flow begins when a client connects to the server using a TCP socket.  
After registration, the server assigns the user to a default room and handles all later room operations and chat forwarding.

## Sequence Diagram

```mermaid
sequenceDiagram
    participant C1 as Client 1
    participant S as Server
    participant C2 as Client 2

    C1->>S: TCP connect
    C1->>S: register(username)
    S-->>C1: register_ack(default room)

    C2->>S: TCP connect
    C2->>S: register(username)
    S-->>C2: register_ack(default room)

    C1->>S: create_room(project)
    S-->>C1: system(room created)

    C1->>S: invite(C2, project)
    S-->>C2: invite(project)

    C2->>S: switch_room(project)
    S-->>C2: room_joined(project)

    C1->>S: chat("hello")
    S-->>C1: chat("hello")
    S-->>C2: chat("hello")
```

## Text Description
1. A client connects to the server over TCP.
2. The client sends a registration message with a unique username.
3. The server validates the username and places the user into a default room.
4. A user may create a new room.
5. A user may invite another user to that room.
6. The invited user can switch into the room.
7. Any chat message is sent to the server.
8. The server forwards that message to all users currently in the same room.
9. When a user disconnects, the server removes the user from internal data structures and informs the room.

## Important Note
The server acts as the single coordination point for all communication.  
This means clients do not communicate directly with each other.