import shutil
import os
import requests


def mirror_file(local_file, target_base_url, filename):
    with open(local_file, "rb") as f:
        files = {"file": (filename, f)}
        try:
            requests.post(
                f"{target_base_url}/mirror_receive/{filename}", files=files, timeout=2
            )
        except Exception as e:
            print(f"Mirror error: {e}")
