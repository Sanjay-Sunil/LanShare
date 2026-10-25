import os
import socket

import config
import protocol


class FileSender:
    def __init__(self, history, device_name):
        self.history = history
        self.device_name = device_name

    def send_files(self, host, port, file_paths):
        valid_paths = [path for path in file_paths if os.path.isfile(path)]
        missing_paths = [path for path in file_paths if not os.path.isfile(path)]

        for path in missing_paths:
            print(f"[ERROR] File not found: {path}")

        if not valid_paths:
            print("[ERROR] No valid files to send.")
            return

        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((host, port))
        except OSError as error:
            print(f"[ERROR] Unable to connect to {host}: {error}")
            for path in valid_paths:
                self.history.add_transfer(
                    host, host, os.path.basename(path), 0, "SENT", "FAILED"
                )
            return

        print(f"Connecting to {host} ...")

        try:
            protocol.send_int(client_socket, len(valid_paths))

            total = len(valid_paths)
            for index, path in enumerate(valid_paths, start=1):
                print(f"[{index}/{total}] Sending {os.path.basename(path)}")
                self._send_one_file(client_socket, host, path)

            print(f"{total}/{total} files transferred.")

        finally:
            client_socket.close()

    def _send_one_file(self, client_socket, host, path):
        filename = os.path.basename(path)
        file_size = os.path.getsize(path)

        metadata = {
            "filename": filename,
            "size": file_size,
            "sender": self.device_name,
        }

        try:
            protocol.send_metadata(client_socket, metadata)

            with open(path, "rb") as file:
                while True:
                    chunk = file.read(config.BUFFER_SIZE)
                    if not chunk:
                        break
                    client_socket.sendall(chunk)

            ok, message = protocol.recv_ack(client_socket)

            if ok:
                print("      Transfer successful")
                status = "SUCCESS"
            else:
                print(f"      Transfer failed: {message}")
                status = "FAILED"

        except (ConnectionError, OSError) as error:
            print(f"      Transfer failed: {error}")
            status = "FAILED"

        self.history.add_transfer(host, host, filename, file_size, "SENT", status)
