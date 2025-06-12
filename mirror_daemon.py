import os
import time
import shutil

SOURCE_DIR = "files"
MIRROR_DIR = "mirror_files"

os.makedirs(MIRROR_DIR, exist_ok=True)

last_mtimes = {}


def sync_files():
    global last_mtimes
    for filename in os.listdir(SOURCE_DIR):
        src_path = os.path.join(SOURCE_DIR, filename)
        dst_path = os.path.join(MIRROR_DIR, filename)

        if not os.path.isfile(src_path):
            continue

        mtime = os.path.getmtime(src_path)
        if filename not in last_mtimes or last_mtimes[filename] != mtime:
            shutil.copy2(src_path, dst_path)
            last_mtimes[filename] = mtime
            print(f"Mirrored: {filename}")


def remove_deleted():
    for filename in os.listdir(MIRROR_DIR):
        if not os.path.exists(os.path.join(SOURCE_DIR, filename)):
            os.remove(os.path.join(MIRROR_DIR, filename))
            print(f"Deleted from mirror: {filename}")


if __name__ == "__main__":
    print("Running mirror daemon...")
    while True:
        sync_files()
        remove_deleted()
        time.sleep(1)
