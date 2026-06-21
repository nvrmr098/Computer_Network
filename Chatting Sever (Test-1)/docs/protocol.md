# Detailed Protocol Specification

## Transport Layer Choice
The application uses TCP sockets.  
TCP was selected because chat applications require reliable and ordered delivery of messages.

## Why TCP Was Chosen
TCP guarantees that packets arrive in order and reduces the risk of missing text messages.  
For a messaging application, reliability is more important than lower overhead.

## Pros of TCP
- Reliable delivery
- Ordered delivery
- Connection-oriented communication
- Easier to use for text chat applications

## Cons of TCP
- Higher overhead than UDP
- Slightly more complex connection handling
- Less suitable for highly time-sensitive applications such as live voice streaming

## Application Protocol
At the application layer, messages are exchanged as JSON objects.  
Each message ends with a newline character so the receiver can safely split messages from the TCP stream.

## Common Fields
- `action`: operation type
- `sender`: username of the sender
- `room`: room name
- `target`: invited user where relevant
- `content`: human-readable message body
- `status`: success or error state
- `timestamp`: message creation time
- `extra`: optional list data such as rooms or users

## Protocol Message Examples

### Register
```json
{
  "action": "register",
  "sender": "Alice",
  "room": "",
  "target": "",
  "content": "",
  "status": "ok",
  "timestamp": "2026-06-21 22:00:00"
}
```

### Register Acknowledgement
```json
{
  "action": "register_ack",
  "sender": "Server",
  "room": "general",
  "target": "",
  "content": "Welcome Alice. You joined room 'general'.",
  "status": "ok",
  "timestamp": "2026-06-21 22:00:01",
  "extra": {
    "rooms": ["general", "random"]
  }
}
```

### Chat Message
```json
{
  "action": "chat",
  "sender": "Alice",
  "room": "general",
  "target": "",
  "content": "Hello everyone",
  "status": "ok",
  "timestamp": "2026-06-21 22:00:10"
}
```

### Create Room
```json
{
  "action": "create_room",
  "sender": "Alice",
  "room": "project",
  "target": "",
  "content": "",
  "status": "ok",
  "timestamp": "2026-06-21 22:00:20"
}
```

### Switch Room
```json
{
  "action": "switch_room",
  "sender": "Alice",
  "room": "project",
  "target": "",
  "content": "",
  "status": "ok",
  "timestamp": "2026-06-21 22:00:25"
}
```

### Invite
```json
{
  "action": "invite",
  "sender": "Alice",
  "room": "project",
  "target": "Bob",
  "content": "Alice invited you to room 'project'. Use /join project to enter.",
  "status": "ok",
  "timestamp": "2026-06-21 22:00:30"
}
```

### List Rooms
```json
{
  "action": "list_rooms",
  "sender": "Alice",
  "room": "",
  "target": "",
  "content": "",
  "status": "ok",
  "timestamp": "2026-06-21 22:00:40"
}
```

### Disconnect
```json
{
  "action": "disconnect",
  "sender": "Alice",
  "room": "",
  "target": "",
  "content": "",
  "status": "ok",
  "timestamp": "2026-06-21 22:01:00"
}
```

## Design Rationale
The protocol was designed to be simple and easy to explain.  
JSON improves readability, and the `action` field makes command handling very clear on both the client and server side.