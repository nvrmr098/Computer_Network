# B205 Computer Networks - Task 1 Chat Application

## Overview
This project is a real-time messaging application developed in Python using socket programming and a client-server architecture over TCP.

The application supports:
- Real-time text messaging
- Multiple chat rooms
- Room creation
- Room switching
- User invitations
- Unique usernames
- Multiple connected users
- Server-side logging
- Configuration-based setup

The system is designed as a console-based application, so it runs directly in the terminal without requiring a GUI.

## Project Structure

```text
project-root/
├── docs/
│   ├── architecture.md
│   ├── communication-flow.md
│   ├── protocol.md
│   └── usage.md
├── logs/
│   └── chat.log
├── src/
│   ├── client.py
│   ├── config.py
│   ├── protocol.py
│   └── server.py
├── .gitignore
└── README.md
```

## Technologies Used
- Python 3
- TCP sockets
- JSON-based application messages
- Multithreading for handling multiple clients

## Architecture
The project follows a client-server model.

- The **server** accepts connections from clients, manages chat rooms, validates unique usernames, handles invitations, and forwards messages.
- The **client** provides a terminal interface for users to join the server and send commands or messages.
- The **protocol layer** uses JSON messages for communication between the client and the server.

More details are available in:
- `docs/architecture.md`
- `docs/protocol.md`
- `docs/communication-flow.md`

## Features
- Register with a unique username
- Join the default room when connecting
- View available chat rooms
- Create a new room
- Switch to another room
- Invite another online user to a room
- Send and receive real-time messages
- Display users in the current room
- Log important server events

## Requirements
- Python 3 installed
- No external Python libraries required

## How to Run

### 1. Start the Server
Open a terminal in the `src` folder and run:

```bash
python server.py
```

### 2. Start Clients
Open separate terminals in the same `src` folder and run:

```bash
python client.py
```

Start at least three clients with different usernames for testing.

## Client Commands

```text
/help                       Show all commands
/rooms                      List available rooms
/users                      List users in current room
/create room_name           Create a new room
/join room_name             Switch to another room
/invite username            Invite a user to the current room
/invite username room_name  Invite a user to a specific room
/exit                       Disconnect from the server
```

## Example Test Scenario
1. Start the server.
2. Start three clients with usernames such as Alice, Bob, and Charlie.
3. Send messages in the default room.
4. Create a room using `/create project`.
5. Invite Bob using `/invite Bob project`.
6. Let Bob join the room using `/join project`.
7. Exchange messages in the new room.
8. Verify that only members of the same room receive those messages.

## Logging
Server activity is stored in:

```text
logs/chat.log
```

The log file records important events such as:
- user connections
- disconnections
- room changes
- invitations
- chat activity

## Documentation
Additional technical documentation is included in the `docs` folder:

- `architecture.md` - system architecture design
- `protocol.md` - protocol specification and protocol analysis
- `communication-flow.md` - message flow between client and server
- `usage.md` - installation and usage instructions

## Design Choices
TCP was selected because a chat application requires reliable and ordered message delivery.

A client-server architecture was selected because it simplifies:
- room management
- username validation
- centralized message routing
- logging
- demonstration and testing

## Notes
This project was developed for the B205 Computer Networks module.

The implementation focuses on:
- socket programming
- modular code structure
- readability
- ease of explanation during demonstration
- required networking functionality for Task 1