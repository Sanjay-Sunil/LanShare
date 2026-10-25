import ipaddress
import os

import config
import discovery
from history import HistoryManager
from receiver import FileReceiver
from sender import FileSender


def show_menu(device_name, local_ip):
    print()
    print("=================================")
    print("             LANShare")
    print("=================================")
    print()
    print(f"Device Name : {device_name}")
    print(f"IP Address  : {local_ip}")
    print()
    print("1. Discover and send files")
    print("2. Send using IP address")
    print("3. View transfer history")
    print("4. Show device information")
    print("5. Exit")
    print()


def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def expand_file_paths(raw_paths):
    expanded = []

    for path in raw_paths:
        if os.path.isdir(path):
            for root, _dirs, files in os.walk(path):
                for filename in files:
                    expanded.append(os.path.join(root, filename))
        else:
            expanded.append(path)

    return expanded


def read_file_list():
    raw = input("Enter file or folder paths separated by commas: ").strip()

    if not raw:
        print("[ERROR] No files entered.")
        return []

    raw_paths = [path.strip() for path in raw.split(",") if path.strip()]
    return expand_file_paths(raw_paths)


def select_known_peer(history):
    peers = history.get_known_peers()

    if not peers:
        return None, None

    print()
    print("Known receivers:")
    for index, peer in enumerate(peers, start=1):
        print(f"{index}. {peer['name']:<12} {peer['ip']}")
    print(f"{len(peers) + 1}. Enter a new IP address")
    print()

    choice = input("Select receiver: ").strip()

    if not choice.isdigit():
        print("[ERROR] Invalid selection.")
        return None, "invalid"

    choice = int(choice)

    if choice == len(peers) + 1:
        return None, None

    if choice < 1 or choice > len(peers):
        print("[ERROR] Invalid selection.")
        return None, "invalid"

    peer = peers[choice - 1]
    return peer["ip"], peer["name"]


def handle_discover_and_send(file_sender, history):
    print("Searching for receivers...")
    receivers = discovery.discover_receivers()

    if not receivers:
        print("No receivers found on the network.")
        choice = input("Enter IP manually? (y/n): ").strip().lower()
        if choice == "y":
            handle_manual_send(file_sender, history)
        return

    print()
    print("Available receivers:")
    print()
    for index, receiver in enumerate(receivers, start=1):
        print(f"{index}. {receiver['name']:<12} {receiver['ip']}")
    print(f"{len(receivers) + 1}. Enter IP manually")
    print()

    choice = input("Select receiver: ").strip()

    if not choice.isdigit():
        print("[ERROR] Invalid selection.")
        return

    choice = int(choice)

    if choice == len(receivers) + 1:
        handle_manual_send(file_sender, history)
        return

    if choice < 1 or choice > len(receivers):
        print("[ERROR] Invalid selection.")
        return

    receiver = receivers[choice - 1]
    files = read_file_list()
    if files:
        file_sender.send_files(receiver["ip"], receiver["port"], files, peer_name=receiver["name"])


def handle_manual_send(file_sender, history):
    ip, peer_name = select_known_peer(history)

    if ip is None:
        if peer_name == "invalid":
            return
        ip = input("Receiver IP: ").strip()
        peer_name = None

    if not is_valid_ip(ip):
        print(f"[ERROR] Invalid IP address: {ip}")
        return

    files = read_file_list()
    if files:
        file_sender.send_files(ip, config.TCP_PORT, files, peer_name=peer_name)


def main():
    device_name = config.get_device_name()
    local_ip = config.get_local_ip()

    history = HistoryManager()
    receiver = FileReceiver(history)
    receiver.start()

    discovery_listener = discovery.DiscoveryListener(device_name)
    discovery_listener.start()

    file_sender = FileSender(history, device_name)

    while True:
        show_menu(device_name, local_ip)
        choice = input("Enter choice: ").strip()

        if choice == "1":
            handle_discover_and_send(file_sender, history)
        elif choice == "2":
            handle_manual_send(file_sender, history)
        elif choice == "3":
            history.show_history()
        elif choice == "4":
            print(f"Device Name : {device_name}")
            print(f"IP Address  : {local_ip}")
            print(f"TCP Port    : {config.TCP_PORT}")
            print(f"Discovery Port : {config.DISCOVERY_PORT}")
        elif choice == "5":
            print("Exiting LANShare.")
            break
        else:
            print("[ERROR] Invalid menu choice.")


if __name__ == "__main__":
    main()
