import os
import socket
import threading

import config
import protocol


class FileReceiver:
    def __init__(self, history, receive_folder=config.RECEIVE_FOLDER, port=config.TCP_PORT):
        self.history = history
        self.receive_folder = receive_folder
        self.port = port
        self.server_socket = None

        os.makedirs(self.receive_folder, exist_ok=True)

    def start(self):
        thread = threading.Thread(target=self._run_server, daemon=True)
        thread.start()

    def _run_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(("0.0.0.0", self.port))
        self.server_socket.listen(5)

        while True:
            try:
                client_socket, address = self.server_socket.accept()
            except OSError:
                break

            client_thread = threading.Thread(
                target=self._handle_client, args=(client_socket, address), daemon=True
            )
            client_thread.start()

    def _handle_client(self, client_socket, address):
        peer_ip = address[0]

        try:
            file_count = protocol.recv_int(client_socket)

            for _ in range(file_count):
                self._receive_one_file(client_socket, peer_ip)

        except (ConnectionError, OSError, ValueError) as error:
            print(f"[ERROR] Problem receiving from {peer_ip}: {error}")
        finally:
            client_socket.close()

    def _receive_one_file(self, client_socket, peer_ip):
        metadata = protocol.recv_metadata(client_socket)
        filename = os.path.basename(metadata["filename"])
        file_size = metadata["size"]
        sender_name = metadata.get("sender", peer_ip)

        destination = self._unique_destination(filename)
        temp_path = destination + ".part"

        print(f"Receiving {filename} from {sender_name} ({peer_ip})")

        received = 0
        success = False

        try:
            with open(temp_path, "wb") as out_file:
                remaining = file_size

                while remaining > 0:
                    chunk = client_socket.recv(min(config.BUFFER_SIZE, remaining))

                    if not chunk:
                        raise ConnectionError("Connection closed before file finished")

                    out_file.write(chunk)
                    remaining -= len(chunk)
                    received += len(chunk)

            os.replace(temp_path, destination)
            success = True
            print(f"Saved as {os.path.basename(destination)}")

        except (ConnectionError, OSError) as error:
            print(f"[ERROR] Failed to receive {filename}: {error}")
            if os.path.exists(temp_path):
                os.remove(temp_path)

        status = "SUCCESS" if success else "FAILED"
        protocol.send_ack(client_socket, success)
        self.history.add_transfer(
            sender_name, peer_ip, filename, received, "RECEIVED", status
        )

    def _unique_destination(self, filename):
        destination = os.path.join(self.receive_folder, filename)

        if not os.path.exists(destination):
            return destination

        name, extension = os.path.splitext(filename)
        counter = 1

        while True:
            candidate = os.path.join(self.receive_folder, f"{name}_{counter}{extension}")
            if not os.path.exists(candidate):
                return candidate
            counter += 1
