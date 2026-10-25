import socket

TCP_PORT = 5000
DISCOVERY_PORT = 5001
BUFFER_SIZE = 64 * 1024

RECEIVE_FOLDER = "received"
DATABASE_FILE = "history.db"

DISCOVERY_MESSAGE = "LANSHARE_DISCOVER"
DISCOVERY_TIMEOUT = 2
ACK_OK = "OK"
ACK_ERROR = "ERROR"


def get_device_name():
    return socket.gethostname()


def get_local_ip():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(("8.8.8.8", 80))
        ip = sock.getsockname()[0]
    except OSError:
        ip = "127.0.0.1"
    finally:
        sock.close()
    return ip
