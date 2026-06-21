# Installation and Usage Guide

## Requirements
- Python 3 installed
- No external libraries required
- One server terminal
- At least three client terminals for testing

## Project Location
Open the project folder in VS Code and use the integrated terminal.

## Run the Server
From the repository root:

```bash
cd task1-chat/src
python server.py
```

## Run Client 1
Open a new terminal:

```bash
cd task1-chat/src
python client.py
```

## Run Client 2
Open another terminal:

```bash
cd task1-chat/src
python client.py
```

## Run Client 3
Open another terminal:

```bash
cd task1-chat/src
python client.py
```

## Basic Test Scenario
1. Start the server.
2. Start three clients with unique usernames such as Alice, Bob, and Charlie.
3. Send messages in the default room `general`.
4. Create a new room with `/create project`.
5. Invite another user with `/invite Bob project`.
6. Join the room using `/join project`.
7. Send messages in the new room.
8. Check that only users in the same room receive those messages.

## Client Commands
- `/help` show all commands
- `/rooms` list rooms
- `/users` list users in the current room
- `/create room_name` create a room
- `/join room_name` switch room
- `/invite username` invite user to current room
- `/invite username room_name` invite user to specific room
- `/exit` disconnect

## Logging
The server stores activity logs in:

```text
task1-chat/logs/chat.log
```