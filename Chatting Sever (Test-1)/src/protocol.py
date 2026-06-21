import json
from datetime import datetime


def current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def build_message(action, sender="", room="", target="", content="", status="ok", extra=None):
    """
    Build one protocol message as a JSON string.
    A newline is added at the end so the receiver can split messages safely.
    """
    message = {
        "action": action,
        "sender": sender,
        "room": room,
        "target": target,
        "content": content,
        "status": status,
        "timestamp": current_time()
    }

    if extra is not None:
        message["extra"] = extra

    return json.dumps(message) + "\n"


def extract_messages(text_buffer):
    """
    TCP is a stream, so multiple JSON messages may arrive together.
    This function splits complete newline-based messages and keeps the unfinished part.
    """
    parts = text_buffer.split("\n")
    complete_lines = parts[:-1]
    remaining_buffer = parts[-1]

    messages = []

    for line in complete_lines:
        line = line.strip()
        if not line:
            continue

        try:
            messages.append(json.loads(line))
        except json.JSONDecodeError:
            # Ignore badly formed lines instead of crashing the app.
            pass

    return messages, remaining_buffer