import json
import socket
import threading

import config


class DiscoveryListener:
    def __init__(self, device_name, tcp_port=config.TCP_PORT, port=config.DISCOVERY_PORT):
        self.device_name = device_name
        self.tcp_port = tcp_port
        self.port = port
        self.sock = None

    def start(self):
        thread = threading.Thread(target=self._run, daemon=True)
        thread.start()

    def _run(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("0.0.0.0", self.port))

        while True:
            try:
                data, address = self.sock.recvfrom(1024)
            except OSError:
                break

            if data.decode("utf-8", errors="ignore") == config.DISCOVERY_MESSAGE:
                reply = json.dumps({"name": self.device_name, "tcp_port": self.tcp_port})
                self.sock.sendto(reply.encode("utf-8"), address)


def discover_receivers(timeout=config.DISCOVERY_TIMEOUT, port=config.DISCOVERY_PORT):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.settimeout(timeout)

    sock.sendto(config.DISCOVERY_MESSAGE.encode("utf-8"), ("255.255.255.255", port))

    receivers = []
    seen_ips = set()

    while True:
        try:
            data, address = sock.recvfrom(1024)
        except socket.timeout:
            break

        ip = address[0]
        if ip in seen_ips:
            continue

        try:
            info = json.loads(data.decode("utf-8"))
        except ValueError:
            continue

        seen_ips.add(ip)
        receivers.append({
            "name": info.get("name", "unknown"),
            "ip": ip,
            "port": info.get("tcp_port", config.TCP_PORT),
        })

    sock.close()
    return receivers
