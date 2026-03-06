import os

ROOM_DIR = "rooms"

if not os.path.exists(ROOM_DIR):
    os.makedirs(ROOM_DIR)


def get_room_file(room_id: str):
    return os.path.join(ROOM_DIR, f"{room_id}.txt")


def save_code(room_id: str, code: str):
    file_path = get_room_file(room_id)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code)


def load_code(room_id: str):

    file_path = get_room_file(room_id)

    if not os.path.exists(file_path):
        return ""

    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()