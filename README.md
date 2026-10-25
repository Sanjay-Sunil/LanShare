# LANShare

Terminal-based file transfer between computers on the same local network.

LANShare lets two or more machines on the same Wi-Fi/LAN send files to each
other directly, without any central server. Every running instance acts as
both a sender and a receiver.

## Features

- Terminal menu interface
- TCP-based file transfer (single file or multiple files in one connection)
- UDP broadcast discovery of other LANShare instances on the network
- Manual IP entry as a fallback when discovery is unavailable
- Background receiver thread so the menu stays responsive while files arrive
- SQLite-backed transfer history (sent and received)
- Safe destination filenames and automatic renaming on filename conflicts
- Partial/incomplete transfers are cleaned up instead of left on disk

## Requirements

- Python 3.8+
- No third-party dependencies

## Running

Start the application on each computer:

```bash
python main.py
```

The receiver and discovery listener start automatically in the background.
The menu offers:

```
1. Discover and send files
2. Send using IP address
3. View transfer history
4. Show device information
5. Exit
```

### Sending files

Choose option 1 to search the LAN for other running LANShare instances, or
option 2 to type a receiver's IP address directly. Enter one or more file
paths separated by commas, e.g.:

```
report.pdf,image.png,notes.txt
```

### Receiving files

Nothing needs to be done manually. Incoming files are written into the
`received/` folder. If a file with the same name already exists, the new
file is saved with a numeric suffix (e.g. `report_1.pdf`).

## Project layout

```
lanshare/
├── main.py       entry point and terminal menu
├── sender.py     FileSender: connects out and transmits files
├── receiver.py   FileReceiver: TCP server and file reception
├── discovery.py  UDP broadcast discovery (listener and client)
├── history.py    HistoryManager: SQLite transfer history
├── protocol.py   shared framing helpers used by sender and receiver
├── config.py     ports, buffer size, and local network helpers
└── received/     destination folder for incoming files
```

## Network notes

Some networks (especially public or campus Wi-Fi) apply client isolation or
block UDP broadcasts, which prevents automatic discovery from working. If
that happens, use the manual IP option instead; direct TCP transfer is
unaffected by this limitation. For development and demos, a personal
hotspot or a simple home router is the most reliable setup.

## Out of scope

This is a small, local, terminal-only tool. It intentionally does not
include a GUI, web interface, encryption, authentication, resume support,
or any form of internet-wide transfer.
