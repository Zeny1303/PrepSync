import os
import time

ROOM_DIR = "rooms"
FIVE_HOURS = 5 * 60 * 60


def cleanup_rooms():

    now = time.time()

    for file in os.listdir(ROOM_DIR):

        file_path = os.path.join(ROOM_DIR, file)

        if not os.path.isfile(file_path):
            continue

        last_modified = os.path.getmtime(file_path)

        if now - last_modified > FIVE_HOURS:
            os.remove(file_path)
            print(f"Deleted old room: {file}")