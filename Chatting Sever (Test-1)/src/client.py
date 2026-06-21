import socket
import threading

from config import HOST, PORT, BUFFER_SIZE, ENCODING
from protocol import build_message, extract_messages


current_username = ""
current_room = ""


def print_help():
    print("\nCommands:")
    print("/help                       Show all commands")
    print("/rooms                      List available rooms")
    print("/users                      List users in current room")
    print("/create room_name           Create a new room")
    print("/join room_name             Switch to an existing room")
    print("/invite username            Invite a user to your current room")
    print("/invite username room_name  Invite a user to a specific room")
    print("/exit                       Leave the chat\n")


def receive_messages(client_socket):
    """
    Background thread: keeps receiving and printing messages from the server.
    """
    global current_room

    buffer = ""

    while True:
        try:
            data = client_socket.recv(BUFFER_SIZE)
            if not data:
                print("\nDisconnected from server.")
                break

            buffer += data.decode(ENCODING)
            messages, buffer = extract_messages(buffer)

            for message in messages:
                action = message.get("action", "")
                sender = message.get("sender", "")
                room = message.get("room", "")
                content = message.get("content", "")
                timestamp = message.get("timestamp", "")
                extra = message.get("extra", {})

                if action == "register_ack":
                    if message.get("status") == "ok":
                        current_room = room
                        print(f"\n[{timestamp}] {content}")
                        rooms = extra.get("rooms", [])
                        if rooms:
                            print("Rooms:", ", ".join(rooms))
                        print_help()
                    else:
                        print(f"\n[{timestamp}] Registration failed: {content}")

                elif action == "room_joined":
                    current_room = room
                    print(f"\n[{timestamp}] {content}")
                    users = extra.get("users", [])
                    if users:
                        print("Users in room:", ", ".join(users))

                elif action == "chat":
                    print(f"\n[{timestamp}] ({room}) {sender}: {content}")

                elif action == "system":
                    print(f"\n[{timestamp}] [SYSTEM] {content}")

                elif action == "invite":
                    print(f"\n[{timestamp}] [INVITE] {content}")

                elif action == "rooms_list":
                    rooms = extra.get("rooms", [])
                    print(f"\n[{timestamp}] Available rooms: {', '.join(rooms)}")

                elif action == "users_list":
                    users = extra.get("users", [])
                    print(f"\n[{timestamp}] Users in {room}: {', '.join(users)}")

                else:
                    print(f"\n[{timestamp}] {sender}: {content}")

        except Exception:
            print("\nConnection closed.")
            break


def start_client():
    """
    Connect to server and read terminal input from the user.
    """
    global current_username

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((HOST, PORT))
    except Exception as error:
        print(f"Could not connect to server: {error}")
        return

    username = input("Enter a unique username: ").strip()
    current_username = username

    register_packet = build_message(
        action="register",
        sender=username
    )
    client_socket.sendall(register_packet.encode(ENCODING))

    receiver_thread = threading.Thread(
        target=receive_messages,
        args=(client_socket,),
        daemon=True
    )
    receiver_thread.start()

    while True:
        try:
            user_input = input().strip()

            if not user_input:
                continue

            if user_input == "/help":
                print_help()

            elif user_input == "/rooms":
                packet = build_message(action="list_rooms", sender=current_username)
                client_socket.sendall(packet.encode(ENCODING))

            elif user_input == "/users":
                packet = build_message(action="list_users", sender=current_username)
                client_socket.sendall(packet.encode(ENCODING))

            elif user_input.startswith("/create "):
                room_name = user_input.split(" ", 1)[1].strip().lower()
                packet = build_message(
                    action="create_room",
                    sender=current_username,
                    room=room_name
                )
                client_socket.sendall(packet.encode(ENCODING))

            elif user_input.startswith("/join "):
                room_name = user_input.split(" ", 1)[1].strip().lower()
                packet = build_message(
                    action="switch_room",
                    sender=current_username,
                    room=room_name
                )
                client_socket.sendall(packet.encode(ENCODING))

            elif user_input.startswith("/invite "):
                parts = user_input.split()

                if len(parts) == 2:
                    target_username = parts[1]
                    packet = build_message(
                        action="invite",
                        sender=current_username,
                        target=target_username
                    )
                    client_socket.sendall(packet.encode(ENCODING))

                elif len(parts) == 3:
                    target_username = parts[1]
                    room_name = parts[2].lower()
                    packet = build_message(
                        action="invite",
                        sender=current_username,
                        target=target_username,
                        room=room_name
                    )
                    client_socket.sendall(packet.encode(ENCODING))

                else:
                    print("Usage: /invite username OR /invite username room_name")

            elif user_input == "/exit":
                packet = build_message(action="disconnect", sender=current_username)
                client_socket.sendall(packet.encode(ENCODING))
                break

            else:
                packet = build_message(
                    action="chat",
                    sender=current_username,
                    content=user_input
                )
                client_socket.sendall(packet.encode(ENCODING))

        except KeyboardInterrupt:
            try:
                packet = build_message(action="disconnect", sender=current_username)
                client_socket.sendall(packet.encode(ENCODING))
            except Exception:
                pass
            break
        except Exception as error:
            print(f"Error: {error}")
            break

    client_socket.close()
    print("You left the chat.")


if __name__ == "__main__":
    start_client()