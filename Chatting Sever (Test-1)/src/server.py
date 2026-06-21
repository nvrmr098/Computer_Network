import socket
import threading
import logging

from config import HOST, PORT, BUFFER_SIZE, ENCODING, DEFAULT_ROOMS, LOG_FILE
from protocol import build_message, extract_messages


# Maps client sockets to usernames.
clients = {}

# Maps usernames to client sockets for quick lookup.
user_sockets = {}

# Maps client sockets to their current room.
client_rooms = {}

# Each room stores the sockets of users inside it.
rooms = {room_name: set() for room_name in DEFAULT_ROOMS}

# Stores invitations: username -> set of room names.
invitations = {}

# Lock protects shared data structures in multi-threaded code.
data_lock = threading.Lock()


logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def send_packet(client_socket, packet_text):
    """
    Send one complete message to a client.
    Returns True on success, False on failure.
    """
    try:
        client_socket.sendall(packet_text.encode(ENCODING))
        return True
    except Exception:
        return False


def send_system(client_socket, content):
    """
    Send a server-generated text message to one client.
    """
    send_packet(
        client_socket,
        build_message(
            action="system",
            sender="Server",
            content=content
        )
    )


def broadcast_to_room(room_name, packet_text, exclude_socket=None):
    """
    Send one packet to all users in a room.
    """
    with data_lock:
        members = list(rooms.get(room_name, set()))

    for member_socket in members:
        if member_socket != exclude_socket:
            send_packet(member_socket, packet_text)


def get_username(client_socket):
    with data_lock:
        return clients.get(client_socket, "Unknown")


def get_current_room(client_socket):
    with data_lock:
        return client_rooms.get(client_socket)


def list_rooms():
    with data_lock:
        return sorted(rooms.keys())


def list_users_in_room(room_name):
    with data_lock:
        names = []
        for member_socket in rooms.get(room_name, set()):
            username = clients.get(member_socket)
            if username:
                names.append(username)
    return sorted(names)


def register_user(client_socket, username):
    """
    Register a new client with a unique username.
    """
    username = username.strip()

    if not username:
        send_packet(
            client_socket,
            build_message(
                action="register_ack",
                sender="Server",
                status="error",
                content="Username cannot be empty."
            )
        )
        return False

    with data_lock:
        if username in user_sockets:
            send_packet(
                client_socket,
                build_message(
                    action="register_ack",
                    sender="Server",
                    status="error",
                    content="Username already exists. Choose another one."
                )
            )
            return False

        clients[client_socket] = username
        user_sockets[username] = client_socket
        invitations[username] = set()

        first_room = DEFAULT_ROOMS[0]
        client_rooms[client_socket] = first_room
        rooms[first_room].add(client_socket)

    send_packet(
        client_socket,
        build_message(
            action="register_ack",
            sender="Server",
            room=first_room,
            status="ok",
            content=f"Welcome {username}. You joined room '{first_room}'.",
            extra={"rooms": list_rooms()}
        )
    )

    broadcast_to_room(
        first_room,
        build_message(
            action="system",
            sender="Server",
            room=first_room,
            content=f"{username} joined the room."
        ),
        exclude_socket=client_socket
    )

    logging.info(f"User registered: {username}")
    return True


def create_room(client_socket, room_name):
    """
    Create a new room if it does not already exist.
    """
    room_name = room_name.strip().lower()

    if not room_name:
        send_system(client_socket, "Room name cannot be empty.")
        return

    with data_lock:
        if room_name in rooms:
            send_system(client_socket, f"Room '{room_name}' already exists.")
            return

        rooms[room_name] = set()

    logging.info(f"Room created: {room_name}")
    send_system(client_socket, f"Room '{room_name}' created successfully.")


def switch_room(client_socket, room_name):
    """
    Move a user from the current room to another existing room.
    """
    room_name = room_name.strip().lower()

    if not room_name:
        send_system(client_socket, "Please provide a room name.")
        return

    with data_lock:
        if room_name not in rooms:
            send_system(client_socket, f"Room '{room_name}' does not exist.")
            return

        old_room = client_rooms.get(client_socket)
        username = clients.get(client_socket, "Unknown")

        if old_room == room_name:
            send_system(client_socket, f"You are already in room '{room_name}'.")
            return

        if old_room in rooms:
            rooms[old_room].discard(client_socket)

        rooms[room_name].add(client_socket)
        client_rooms[client_socket] = room_name

    if old_room:
        broadcast_to_room(
            old_room,
            build_message(
                action="system",
                sender="Server",
                room=old_room,
                content=f"{username} left the room."
            ),
            exclude_socket=client_socket
        )

    broadcast_to_room(
        room_name,
        build_message(
            action="system",
            sender="Server",
            room=room_name,
            content=f"{username} joined the room."
        ),
        exclude_socket=client_socket
    )

    send_packet(
        client_socket,
        build_message(
            action="room_joined",
            sender="Server",
            room=room_name,
            content=f"You switched to room '{room_name}'.",
            extra={"users": list_users_in_room(room_name)}
        )
    )

    logging.info(f"{username} switched from {old_room} to {room_name}")


def invite_user(client_socket, target_username, room_name=None):
    """
    Send a room invitation to another online user.
    """
    sender_name = get_username(client_socket)
    current_room = get_current_room(client_socket)

    if room_name is None or not room_name.strip():
        room_name = current_room
    else:
        room_name = room_name.strip().lower()

    if not room_name:
        send_system(client_socket, "You are not in any room.")
        return

    with data_lock:
        if room_name not in rooms:
            send_system(client_socket, f"Room '{room_name}' does not exist.")
            return

        target_socket = user_sockets.get(target_username)

        if not target_socket:
            send_system(client_socket, f"User '{target_username}' is not online.")
            return

        invitations[target_username].add(room_name)

    send_system(client_socket, f"Invitation sent to {target_username} for room '{room_name}'.")

    send_packet(
        target_socket,
        build_message(
            action="invite",
            sender=sender_name,
            room=room_name,
            target=target_username,
            content=f"{sender_name} invited you to room '{room_name}'. Use /join {room_name} to enter."
        )
    )

    logging.info(f"{sender_name} invited {target_username} to room {room_name}")


def send_rooms_list(client_socket):
    """
    Send all available rooms to one client.
    """
    send_packet(
        client_socket,
        build_message(
            action="rooms_list",
            sender="Server",
            content="Available rooms",
            extra={"rooms": list_rooms()}
        )
    )


def send_users_list(client_socket):
    """
    Send all users in the current room to one client.
    """
    room_name = get_current_room(client_socket)

    if not room_name:
        send_system(client_socket, "You are not in any room.")
        return

    send_packet(
        client_socket,
        build_message(
            action="users_list",
            sender="Server",
            room=room_name,
            content=f"Users in room '{room_name}'",
            extra={"users": list_users_in_room(room_name)}
        )
    )


def handle_chat(client_socket, content):
    """
    Broadcast a normal chat message to everyone in the sender's current room.
    """
    username = get_username(client_socket)
    room_name = get_current_room(client_socket)

    if not room_name:
        send_system(client_socket, "Join a room before sending messages.")
        return

    content = content.strip()
    if not content:
        return

    packet = build_message(
        action="chat",
        sender=username,
        room=room_name,
        content=content
    )

    broadcast_to_room(room_name, packet)
    logging.info(f"[{room_name}] {username}: {content}")


def remove_client(client_socket):
    """
    Clean up disconnected client data.
    """
    with data_lock:
        username = clients.get(client_socket)
        room_name = client_rooms.get(client_socket)

        if room_name in rooms:
            rooms[room_name].discard(client_socket)

        if username and username in user_sockets:
            del user_sockets[username]

        if username and username in invitations:
            del invitations[username]

        if client_socket in client_rooms:
            del client_rooms[client_socket]

        if client_socket in clients:
            del clients[client_socket]

    if username and room_name:
        broadcast_to_room(
            room_name,
            build_message(
                action="system",
                sender="Server",
                room=room_name,
                content=f"{username} disconnected."
            ),
            exclude_socket=client_socket
        )
        logging.info(f"Client disconnected: {username}")


def process_message(client_socket, message):
    """
    Execute a command sent by a client.
    """
    action = message.get("action", "")

    if action == "register":
        return register_user(client_socket, message.get("sender", ""))

    if action == "chat":
        handle_chat(client_socket, message.get("content", ""))
        return True

    if action == "create_room":
        create_room(client_socket, message.get("room", ""))
        return True

    if action == "switch_room":
        switch_room(client_socket, message.get("room", ""))
        return True

    if action == "invite":
        invite_user(
            client_socket,
            message.get("target", "").strip(),
            message.get("room", "")
        )
        return True

    if action == "list_rooms":
        send_rooms_list(client_socket)
        return True

    if action == "list_users":
        send_users_list(client_socket)
        return True

    if action == "disconnect":
        return False

    send_system(client_socket, "Unknown command.")
    return True


def handle_client(client_socket, address):
    """
    Each connected client is handled in a separate thread.
    """
    print(f"Connection from {address}")
    logging.info(f"Incoming connection from {address}")

    buffer = ""
    registered = False

    try:
        while True:
            data = client_socket.recv(BUFFER_SIZE)
            if not data:
                break

            buffer += data.decode(ENCODING)
            messages, buffer = extract_messages(buffer)

            for message in messages:
                if not registered:
                    if message.get("action") != "register":
                        send_system(client_socket, "Please register first.")
                        continue

                    registered = register_user(client_socket, message.get("sender", ""))
                    if not registered:
                        continue
                else:
                    keep_running = process_message(client_socket, message)
                    if not keep_running:
                        raise ConnectionAbortedError("Client requested disconnect")

    except Exception as error:
        logging.error(f"Client error at {address}: {error}")

    finally:
        remove_client(client_socket)
        try:
            client_socket.close()
        except Exception:
            pass


def start_server():
    """
    Main server startup function.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)

    print(f"Server is running on {HOST}:{PORT}")
    print(f"Default rooms: {', '.join(DEFAULT_ROOMS)}")
    logging.info(f"Server started on {HOST}:{PORT}")

    try:
        while True:
            client_socket, address = server_socket.accept()
            thread = threading.Thread(
                target=handle_client,
                args=(client_socket, address),
                daemon=True
            )
            thread.start()

    except KeyboardInterrupt:
        print("\nServer stopped.")

    finally:
        server_socket.close()
        logging.info("Server shutdown.")


if __name__ == "__main__":
    start_server()