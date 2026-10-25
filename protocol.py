import json
import struct


def recv_exact(sock, size):
    data = b""

    while len(data) < size:
        chunk = sock.recv(size - len(data))

        if not chunk:
            raise ConnectionError("Connection closed before expected data arrived")

        data += chunk

    return data


def send_int(sock, number):
    sock.sendall(struct.pack("!I", number))


def recv_int(sock):
    data = recv_exact(sock, 4)
    return struct.unpack("!I", data)[0]


def send_metadata(sock, metadata):
    payload = json.dumps(metadata).encode("utf-8")
    send_int(sock, len(payload))
    sock.sendall(payload)


def recv_metadata(sock):
    length = recv_int(sock)
    payload = recv_exact(sock, length)
    return json.loads(payload.decode("utf-8"))


def send_ack(sock, ok, message=""):
    status = "OK" if ok else "ERROR"
    send_metadata(sock, {"status": status, "message": message})


def recv_ack(sock):
    ack = recv_metadata(sock)
    return ack.get("status") == "OK", ack.get("message", "")
