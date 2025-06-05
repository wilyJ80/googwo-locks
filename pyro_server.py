from Pyro5.api import expose, Daemon
from collections import defaultdict
import threading


@expose
class DocManager:
    def __init__(self):
        self.locks = defaultdict(lambda: None)
        self.lock = threading.Lock()

    def request_lock(self, filename, ip):
        with self.lock:
            if self.locks[filename] in (None, ip):
                self.locks[filename] = ip
                return True
            return False

    def release_lock(self, filename, ip):
        with self.lock:
            if self.locks[filename] == ip:
                self.locks[filename] = None

    def get_lock_info(self, filename):
        with self.lock:
            return self.locks[filename]


if __name__ == "__main__":
    daemon = Daemon(host="0.0.0.0", port=9090)
    uri = daemon.register(DocManager(), "docmanager")
    print("Pyro server running at:", uri)
    daemon.requestLoop()
