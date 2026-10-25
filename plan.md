# LANShare Mini Project — End-to-End Execution Plan

## 1. Project Title

**LANShare — Terminal-Based File Transfer Between Computers on the Same Wi-Fi**

Course: **ICS 214 — IT Workshop III**

---

## 2. Project Objective

Build a small Python terminal application that allows two or more computers connected to the same local Wi-Fi/LAN to transfer files directly.

The project must remain within the scope of the ICS 214 syllabus. It is intended as a **mini project for demonstration and evaluation**, not as a production-grade file-sharing application.

The application should allow a user to:

1. Start the application from a terminal.
2. Discover receivers available on the same LAN.
3. Select a discovered receiver or enter the receiver's IP address manually.
4. Select one file or multiple files.
5. Transfer those files to the selected computer.
6. Store incoming files in a dedicated local directory.
7. Record every transfer in a local history database.
8. View transfer history from the terminal.
9. Continue receiving files while the terminal application is running.

---

## 3. Why This Project Fits the ICS 214 Syllabus

This project intentionally combines topics directly covered in the supplied course material.

### Session 1–2: Python Fundamentals

Used for:

- Variables
- Input/output
- Operators
- Conditions
- Loops
- Terminal menus
- Validation logic

### Session 3: File Processing

Session 3 covers:

- Reading files
- Writing files
- File processing
- Text and CSV files

LANShare applies the same file-processing concepts to binary files.

Files will be opened using:

```python
open(path, "rb")
```

and received files will be created using:

```python
open(path, "wb")
```

### Session 4–6: Lists, Dictionaries, Tuples, Strings

Used for:

- Maintaining the list of selected files
- Maintaining discovered receivers
- Storing metadata
- Manipulating filenames
- Formatting terminal output
- Processing IP addresses and paths

### Session 7: Functions and Modules

The project will be divided into reusable functions and Python modules.

Examples:

```python
discover_receivers()
send_files()
receive_files()
save_history()
show_history()
```

### Session 8: Object-Oriented Programming

Session 8 covers classes and objects.

The project may organize functionality using small classes such as:

```text
FileSender
FileReceiver
HistoryManager
```

OOP should remain simple and should not be used merely to increase complexity.

### Session 9: Database Processing and Network Programming

This is the **core syllabus connection**.

Session 9 covers:

- SQLite
- Database connections
- Creating tables
- Queries
- Network programming
- Sockets
- Client/server communication
- TCP
- UDP

The course material demonstrates TCP server/client operations using:

```python
socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bind()
listen()
accept()
connect()
send()
recv()
```

LANShare will use these same concepts for file transfer.

SQLite will be used to maintain transfer history.

### Session 10: FTP and Multithreading

Session 10 covers:

- File Transfer Protocol concepts
- Upload/download concepts
- Binary file transfer
- Threads
- Multiple threads
- Handling multiple client connections

LANShare does **not need to implement a full FTP server**.

Instead, it will implement file transfer using TCP sockets while applying the same client/server file-transfer concepts taught in the FTP section.

Threading will be used so that the receiver can continue listening while the terminal menu is active.

---

# 4. Final Project Scope

## Required Features

The final system will support:

- Terminal-based interface
- TCP file transfer
- UDP receiver discovery
- Manual IP entry
- Single-file transfer
- Bulk file transfer
- Background file receiving
- Local SQLite transfer history
- Transfer status reporting
- Error handling
- Dedicated received-file directory

## Explicitly Out of Scope

Do **not** add the following:

- GUI
- Web interface
- Mobile application
- Cloud storage
- User accounts
- Authentication server
- Internet-wide file transfer
- Encryption protocols
- File synchronization
- Resume interrupted transfer
- Distributed database
- NAT traversal
- Peer-to-peer internet discovery
- Advanced compression
- Production security infrastructure

Keeping these out prevents the project from going beyond the intended syllabus and mini-project scale.

---

# 5. Proposed System Architecture

Every running LANShare instance acts as both:

- **Sender**
- **Receiver**

There is no central server.

```text
                     SAME LOCAL NETWORK / WI-FI

        Computer A                              Computer B

     +--------------+                       +--------------+
     |   LANShare   |                       |   LANShare   |
     +--------------+                       +--------------+
            |                                      |
            |---- UDP Discovery ------------------>|
            |<--- Discovery Reply -----------------|
            |                                      |
            |========= TCP CONNECTION ============>|
            |                                      |
            |--- Metadata ------------------------>|
            |--- File bytes ---------------------->|
            |<-- ACK ------------------------------|
            |                                      |
            |--- Update SQLite history             |
            |                       Update history--|
```

---

# 6. Why TCP and UDP Are Both Used

## TCP

TCP will be used for actual file transfer.

Reason:

- Reliable
- Ordered
- Connection-oriented
- Appropriate for files
- Explicitly covered in the course networking material

Python socket type:

```python
socket.socket(socket.AF_INET, socket.SOCK_STREAM)
```

Typical workflow:

```text
SERVER

socket()
bind()
listen()
accept()
recv()
send()
close()

CLIENT

socket()
connect()
send()
recv()
close()
```

## UDP

UDP will only be used for receiver discovery.

Python socket type:

```python
socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
```

Discovery does not require a permanent connection.

If UDP broadcast is unavailable on a network, users can still enter the receiver IP manually.

---

# 7. Recommended Port Allocation

Use two ports.

```text
TCP_FILE_PORT = 5000
UDP_DISCOVERY_PORT = 5001
```

Meaning:

```text
5000 -> actual file transfers
5001 -> discovery requests and replies
```

Avoid using privileged ports below 1024.

---

# 8. Project Directory Structure

Create the project as:

```text
lanshare/
│
├── main.py
├── sender.py
├── receiver.py
├── discovery.py
├── history.py
├── protocol.py
├── config.py
│
├── received/
│
├── history.db
│
└── README.md
```

## File Responsibilities

### `main.py`

Responsible for:

- Starting LANShare
- Starting receiver threads
- Showing terminal menu
- Taking user input
- Calling other modules

### `sender.py`

Responsible for:

- Connecting to another computer
- Sending metadata
- Reading files
- Sending file chunks
- Handling acknowledgements

### `receiver.py`

Responsible for:

- Creating TCP server socket
- Listening for incoming connections
- Receiving metadata
- Receiving file bytes
- Saving files
- Sending acknowledgements

### `discovery.py`

Responsible for:

- Sending UDP discovery broadcasts
- Listening for discovery requests
- Responding with device information
- Building receiver list

### `history.py`

Responsible for:

- Creating SQLite database
- Creating history table
- Inserting transfer records
- Displaying history

### `protocol.py`

Responsible for:

- Message framing
- Metadata serialization
- Exact-length receiving
- Shared sender/receiver protocol helpers

### `config.py`

Contains:

```python
TCP_PORT = 5000
DISCOVERY_PORT = 5001
BUFFER_SIZE = 65536
RECEIVE_FOLDER = "received"
```

---

# 9. Terminal User Experience

Initial menu:

```text
=================================
             LANShare
=================================

Device Name : laptop-A
IP Address  : 192.168.1.10

1. Discover receivers
2. Send files
3. View transfer history
4. Show device information
5. Exit

Enter choice:
```

## Receiver Discovery Example

```text
Searching for receivers...

Available receivers:

1. laptop-B     192.168.1.12
2. laptop-C     192.168.1.15
3. Enter IP manually

Select receiver:
```

## File Selection Example

For a mini project, terminal file-path input is sufficient.

```text
Enter file paths separated by commas:

report.pdf,image.png,notes.txt
```

The program converts this into:

```python
files = [
    "report.pdf",
    "image.png",
    "notes.txt"
]
```

Validate every file before starting transfer.

---

# 10. Transfer Protocol Design

TCP is a byte stream.

A single `recv()` call does **not** necessarily correspond to one `send()` call.

Therefore the program needs a small application-level protocol.

## Connection Format

```text
TCP CONNECTION

4 bytes
+--------------------------+
| Number of files          |
+--------------------------+

For each file:

4 bytes
+--------------------------+
| Metadata length          |
+--------------------------+

N bytes
+--------------------------+
| Metadata JSON            |
+--------------------------+

file_size bytes
+--------------------------+
| Actual file data         |
+--------------------------+

Receiver response
+--------------------------+
| ACK / ERROR              |
+--------------------------+
```

---

# 11. File Metadata

Metadata for every file contains:

```json
{
    "filename": "report.pdf",
    "size": 102400
}
```

Possible additional field:

```json
{
    "filename": "report.pdf",
    "size": 102400,
    "sender": "laptop-A"
}
```

Keep metadata minimal.

---

# 12. Binary Integer Encoding

Use `struct` to send fixed-size integers.

Example:

```python
import struct

packed = struct.pack("!I", number)
```

`!I` means:

- network byte order
- unsigned 4-byte integer

Receiver:

```python
number = struct.unpack("!I", data)[0]
```

This is a small implementation utility used to make the socket protocol reliable.

---

# 13. Essential Helper: `recv_exact()`

TCP may return fewer bytes than requested.

Therefore implement:

```python
def recv_exact(sock, size):
    data = b""

    while len(data) < size:
        chunk = sock.recv(size - len(data))

        if not chunk:
            raise ConnectionError("Connection closed")

        data += chunk

    return data
```

This function should be reused whenever fixed-size protocol data must be received.

---

# 14. Single File Transfer Algorithm

## Sender

```text
START

Select receiver
Select file

Check file exists

Connect using TCP

Get:
    filename
    filesize

Send:
    file count = 1

Send:
    metadata length

Send:
    metadata

Open file in binary mode

WHILE data remains
    read chunk
    send chunk
END WHILE

Wait for acknowledgement

Save result in history

Close connection

END
```

## Receiver

```text
START SERVER

Create socket
Bind TCP port
Listen

WHILE program running

    Accept connection

    Receive file count

    FOR every file

        Receive metadata length

        Receive metadata

        Get filename and file size

        Open destination file

        WHILE remaining bytes > 0

            Receive chunk
            Write chunk

            remaining =
                remaining - received bytes

        END WHILE

        Send acknowledgement

        Save transfer history

    END FOR

END WHILE
```

---

# 15. Bulk File Transfer

Bulk upload should **not** create one new TCP connection per file.

Use one TCP connection for the complete batch.

Example:

```text
Connection opened

File count = 3

report.pdf
   metadata
   bytes
   ACK

image.png
   metadata
   bytes
   ACK

notes.txt
   metadata
   bytes
   ACK

Connection closed
```

This gives a simple and clean bulk-transfer implementation.

---

# 16. File Chunking

Do not load an entire file into memory.

Use chunks.

Recommended:

```python
BUFFER_SIZE = 64 * 1024
```

which is:

```text
65536 bytes
```

Sender:

```python
with open(path, "rb") as file:

    while True:
        chunk = file.read(BUFFER_SIZE)

        if not chunk:
            break

        sock.sendall(chunk)
```

Receiver:

```python
remaining = file_size

while remaining > 0:

    chunk = sock.recv(
        min(BUFFER_SIZE, remaining)
    )

    if not chunk:
        raise ConnectionError()

    file.write(chunk)

    remaining -= len(chunk)
```

---

# 17. Receiver Discovery Design

Receiver discovery uses UDP broadcast.

## Discovery Request

Sender broadcasts:

```text
LANSHARE_DISCOVER
```

to:

```text
255.255.255.255:5001
```

Every running LANShare instance listening on UDP port 5001 detects the request.

It replies directly to the sender with something like:

```json
{
    "name": "laptop-B",
    "tcp_port": 5000
}
```

The sender gets the receiver IP automatically from:

```python
data, address = sock.recvfrom(...)
```

where:

```python
address[0]
```

contains the sender IP.

---

# 18. Discovery Algorithm

## Discovering Computer

```text
Create UDP socket

Enable broadcast

Send:
LANSHARE_DISCOVER

Wait approximately 2 seconds

Collect replies

Store each receiver:

{
    name,
    ip,
    port
}

Remove duplicate IPs

Display receiver list
```

## Receiver Discovery Listener

```text
Create UDP socket

Bind UDP port 5001

WHILE application is running

    receive request

    IF request == LANSHARE_DISCOVER

        send:
        device name + TCP port

END WHILE
```

---

# 19. Manual IP Mode

Always include:

```text
Enter receiver IP manually
```

Example:

```text
Receiver IP: 192.168.1.12
```

The sender then connects to:

```python
("192.168.1.12", 5000)
```

This is important because some Wi-Fi networks block UDP broadcasts.

---

# 20. Transfer History Database

Use SQLite.

Database:

```text
history.db
```

Table:

```sql
CREATE TABLE IF NOT EXISTS transfers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    peer_name TEXT,
    peer_ip TEXT,
    filename TEXT,
    file_size INTEGER,
    direction TEXT,
    status TEXT,
    timestamp TEXT
);
```

Example records:

```text
+----+-------------+----------------+------------+-----------+---------+
| ID | Filename    | Peer           | Direction  | Size      | Status  |
+----+-------------+----------------+------------+-----------+---------+
| 1  | report.pdf  | 192.168.1.12   | SENT       | 102400    | SUCCESS |
| 2  | image.png   | 192.168.1.12   | SENT       | 230000    | SUCCESS |
| 3  | notes.txt   | 192.168.1.15   | RECEIVED   | 5200      | SUCCESS |
+----+-------------+----------------+------------+-----------+---------+
```

---

# 21. History Functions

Implement:

```python
initialize_database()
```

```python
add_transfer(
    peer_name,
    peer_ip,
    filename,
    size,
    direction,
    status
)
```

```python
show_history()
```

Optional:

```python
clear_history()
```

Do not make history functionality more complicated than necessary.

---

# 22. Threading Architecture

The main challenge is that the application must:

1. Display menus.
2. Listen for incoming TCP transfers.
3. Listen for UDP discovery requests.

These cannot all block the main program at the same time.

Use three logical execution flows.

```text
MAIN THREAD
    |
    +---- Terminal menu
    |
    +---- TCP receiver thread
    |
    +---- UDP discovery listener thread
```

At startup:

```python
tcp_thread = threading.Thread(
    target=start_tcp_server,
    daemon=True
)

udp_thread = threading.Thread(
    target=start_discovery_listener,
    daemon=True
)

tcp_thread.start()
udp_thread.start()
```

The main thread continues displaying the menu.

This directly demonstrates the threading concepts covered in Session 10.

---

# 23. Optional Multiple-Client Support

If another computer connects while one file transfer is happening, the TCP server can create one thread per accepted connection.

Pattern:

```python
while True:

    client_socket, address = server.accept()

    thread = threading.Thread(
        target=handle_client,
        args=(client_socket, address),
        daemon=True
    )

    thread.start()
```

This is within the multithreading concepts taught in the syllabus.

For the minimum viable submission, supporting one transfer at a time is acceptable unless the instructor specifically requires simultaneous transfers.

---

# 24. Filename Safety

Received files must always go into:

```text
received/
```

Never directly trust a sender-provided path.

Convert:

```text
/home/user/documents/report.pdf
```

to:

```text
report.pdf
```

using:

```python
os.path.basename(filename)
```

Final destination:

```python
received/report.pdf
```

---

# 25. Duplicate Filename Handling

If:

```text
report.pdf
```

already exists, do not silently overwrite it.

Rename the new file:

```text
report_1.pdf
report_2.pdf
report_3.pdf
```

Algorithm:

```text
IF filename does not exist:
    use filename

ELSE:
    add increasing number
    until unused filename is found
```

This is enough for the project.

---

# 26. Error Handling

Handle at least these cases.

## Sender-side

```text
File does not exist
Invalid IP address
Receiver unavailable
Connection refused
Connection interrupted
File cannot be opened
```

## Receiver-side

```text
Connection interrupted
Invalid metadata
Incomplete file
Cannot create destination file
```

Use:

```python
try:
    ...
except ...
```

Do not allow one failed transfer to terminate the entire application.

---

# 27. Failed File Cleanup

Suppose the sender claims:

```text
size = 100 MB
```

but the connection closes after 20 MB.

The partial file should not remain as if it were valid.

Recommended sequence:

```text
Create temporary file

report.pdf.part

receive file

IF full size received:
    rename to report.pdf
ELSE:
    delete report.pdf.part
```

This is a practical addition without adding major complexity.

---

# 28. Transfer Acknowledgement

After successfully receiving a complete file, receiver sends:

```text
OK
```

If failed:

```text
ERROR
```

Sender should only log:

```text
SUCCESS
```

after receiving the acknowledgement.

This prevents falsely marking incomplete transfers as successful.

---

# 29. Transfer History Rules

For every file attempt:

Sender records:

```text
direction = SENT
```

Receiver records:

```text
direction = RECEIVED
```

Status can be:

```text
SUCCESS
FAILED
```

Optional:

```text
CANCELLED
```

For this mini project, `SUCCESS` and `FAILED` are enough.

---

# 30. Recommended Development Order

Do **not** try to implement the entire application at once.

Follow this order exactly.

---

# PHASE 0 — Environment Setup

## Goal

Create project structure.

Commands:

```bash
mkdir -p lanshare/received
cd lanshare

touch main.py
touch sender.py
touch receiver.py
touch discovery.py
touch history.py
touch protocol.py
touch config.py
touch README.md
```

Check Python:

```bash
python --version
```

No third-party dependencies should be required.

### Completion Criteria

```text
Project directory exists.
Python runs.
All modules import without errors.
```

---

# PHASE 1 — Basic TCP Communication

## Goal

Prove that two Python programs can communicate.

First build:

```text
receiver.py
sender.py
```

Receiver:

```text
socket
bind
listen
accept
recv
send
close
```

Sender:

```text
socket
connect
send
recv
close
```

Initially send only:

```text
Hello from LANShare
```

### Local Test

Run receiver:

```bash
python receiver.py
```

Then sender:

```bash
python sender.py
```

using:

```text
127.0.0.1
```

### LAN Test

Find receiver's local IP.

Example:

```text
192.168.1.12
```

Connect from another computer.

### Completion Criteria

```text
Computer A sends a message.
Computer B receives it.
Computer B replies.
Computer A receives reply.
```

Do not continue until this works.

---

# PHASE 2 — Single Binary File Transfer

## Goal

Transfer one arbitrary file.

Start with a small file:

```text
sample.txt
```

Then test:

```text
image.jpg
document.pdf
```

Implementation:

1. Sender determines filename.
2. Sender determines size.
3. Sender sends metadata.
4. Receiver reads metadata.
5. Sender reads file in chunks.
6. Receiver writes chunks.
7. Receiver verifies expected byte count.
8. Receiver sends ACK.

### Completion Criteria

Transfer:

```text
TXT
PDF
JPG/PNG
```

and verify each opens correctly.

---

# PHASE 3 — Create Protocol Helpers

## Goal

Remove duplicated networking logic.

Implement in:

```text
protocol.py
```

Functions such as:

```python
send_int()
recv_int()
send_metadata()
recv_metadata()
recv_exact()
```

### Completion Criteria

Sender and receiver use the same protocol module.

---

# PHASE 4 — Bulk File Transfer

## Goal

Transfer multiple files through one connection.

Input:

```text
file1.pdf,file2.jpg,file3.txt
```

Convert to list.

Validate all paths.

Send:

```text
number of files
```

Then loop over every file.

### Completion Criteria

At least three files transfer successfully in one operation.

---

# PHASE 5 — SQLite History

## Goal

Persist transfer information.

Create:

```text
history.py
```

On first startup:

```python
initialize_database()
```

After each file:

```python
add_transfer(...)
```

Menu option:

```text
View Transfer History
```

### Completion Criteria

Close the application.

Restart it.

Old history should still appear.

---

# PHASE 6 — Receiver Background Thread

## Goal

Make LANShare receive files while the menu remains usable.

Move TCP server into:

```python
start_tcp_server()
```

Start it using:

```python
threading.Thread(...)
```

The main thread should remain available for user input.

### Completion Criteria

While:

```text
LANShare menu
```

is visible, another computer can send a file to the machine.

---

# PHASE 7 — UDP Discovery

## Goal

Automatically find LANShare receivers.

Implement:

```python
start_discovery_listener()
```

and:

```python
discover_receivers()
```

Display result:

```text
1. laptop-B 192.168.1.12
2. laptop-C 192.168.1.15
3. Enter IP manually
```

### Completion Criteria

Two running LANShare machines discover each other on a suitable LAN.

---

# PHASE 8 — Integrate Terminal Menu

## Goal

Combine the modules.

Recommended main menu:

```text
1. Discover and send files
2. Send using IP address
3. View transfer history
4. Show local device information
5. Exit
```

Suggested structure:

```python
def main():

    initialize_database()

    start_receiver_thread()
    start_discovery_thread()

    while True:

        show_menu()

        choice = input(...)

        if choice == "1":
            ...

        elif choice == "2":
            ...

        elif choice == "3":
            ...

        elif choice == "4":
            ...

        elif choice == "5":
            break
```

### Completion Criteria

All functionality is accessible from `main.py`.

---

# PHASE 9 — Validation and Error Handling

Add validation after the core application works.

Validate:

```text
Receiver IP
File existence
Empty file list
File size
Connection failure
Invalid menu input
Invalid metadata
```

Use clear messages:

```text
[ERROR] File not found: report.pdf
```

```text
[ERROR] Unable to connect to 192.168.1.12
```

```text
[SUCCESS] report.pdf transferred successfully.
```

---

# PHASE 10 — Final Testing

Perform systematic tests.

## Test 1 — localhost

```text
Sender: localhost
Receiver: localhost
```

Expected:

```text
File received correctly
```

## Test 2 — two computers

```text
Computer A -> Computer B
```

Expected:

```text
File received
History saved
```

## Test 3 — reverse direction

```text
Computer B -> Computer A
```

## Test 4 — bulk files

Transfer:

```text
TXT
PDF
PNG
```

together.

## Test 5 — nonexistent file

Expected:

```text
Rejected before transfer
```

## Test 6 — invalid receiver

Expected:

```text
Connection error handled
Application continues running
```

## Test 7 — duplicate filename

Send the same file twice.

Expected:

```text
report.pdf
report_1.pdf
```

## Test 8 — receiver disconnected

Attempt to send.

Expected:

```text
Failure logged correctly
Application continues
```

## Test 9 — persistent history

Restart application.

Expected:

```text
Previous history remains
```

---

# 31. Recommended Implementation Milestones

## Milestone 1

```text
TCP hello-world works
```

## Milestone 2

```text
One binary file transfers
```

## Milestone 3

```text
Protocol framing is reliable
```

## Milestone 4

```text
Bulk files transfer
```

## Milestone 5

```text
History database works
```

## Milestone 6

```text
Background receiver works
```

## Milestone 7

```text
Receiver discovery works
```

## Milestone 8

```text
Complete terminal application works
```

---

# 32. Suggested Work Distribution

If this is an individual project:

### Stage 1

Networking fundamentals:

```text
sender.py
receiver.py
protocol.py
```

### Stage 2

Storage:

```text
history.py
received/
```

### Stage 3

Discovery:

```text
discovery.py
```

### Stage 4

Integration:

```text
main.py
```

### Stage 5

Testing and documentation.

---

# 33. Approximate Development Time

For a student already familiar with basic Python:

| Task | Approximate Effort |
|---|---:|
| TCP communication | 1 hour |
| Single-file transfer | 1–2 hours |
| Protocol helpers | 1 hour |
| Bulk transfer | 1 hour |
| SQLite history | 1 hour |
| Threading | 1 hour |
| UDP discovery | 1–2 hours |
| Integration | 1 hour |
| Testing/debugging | 2 hours |

Expected total:

```text
9–12 focused hours
```

This is only a planning estimate.

---

# 34. Suggested Build Sessions

## Build Session 1

Finish:

```text
TCP sender
TCP receiver
Hello-world communication
```

## Build Session 2

Finish:

```text
File metadata
File chunking
Single-file transfer
```

## Build Session 3

Finish:

```text
Bulk transfer
Acknowledgements
```

## Build Session 4

Finish:

```text
SQLite database
History display
```

## Build Session 5

Finish:

```text
Threaded receiving
UDP discovery
```

## Build Session 6

Finish:

```text
Terminal UI
Error handling
Testing
README
```

---

# 35. Final Demo Scenario

Use two laptops connected to the same Wi-Fi or hotspot.

## Computer B

Run:

```bash
python main.py
```

The receiver thread begins listening.

## Computer A

Run:

```bash
python main.py
```

Choose:

```text
1. Discover and send files
```

Expected:

```text
Available receivers:

1. laptop-B 192.168.1.12
```

Select:

```text
1
```

Enter:

```text
sample.txt,image.png,report.pdf
```

Expected sender output:

```text
Connecting to laptop-B...

[1/3] Sending sample.txt
      Transfer successful

[2/3] Sending image.png
      Transfer successful

[3/3] Sending report.pdf
      Transfer successful

3/3 files transferred.
```

Computer B should display:

```text
Incoming connection from 192.168.1.10

Receiving sample.txt...
Saved.

Receiving image.png...
Saved.

Receiving report.pdf...
Saved.
```

Then show history on both machines.

This demonstrates almost every important project feature in one demo.

---

# 36. Minimum Viable Project

If time becomes limited, the minimum acceptable version should contain:

```text
TCP file transfer
Single + multiple files
Manual receiver IP
SQLite history
Terminal menu
Background receiver
```

UDP discovery can be added afterward.

This minimum version still strongly demonstrates the main syllabus topics.

---

# 37. Recommended Final Version

The final submission should contain:

```text
Terminal interface
TCP transfer
UDP discovery
Manual IP fallback
Single file transfer
Bulk transfer
SQLite history
Threaded receiver
Basic validation
Dedicated received directory
Duplicate filename handling
```

Do not add unnecessary functionality beyond this.

---

# 38. Important Networking Limitation

Some college/public Wi-Fi networks enable:

```text
AP isolation / client isolation
```

This prevents devices connected to the same access point from directly communicating.

UDP broadcast may also be blocked.

Therefore, during development and demonstration, preferably use:

```text
Laptop A
Laptop B
    |
    +---- Personal hotspot / LAN
```

If automatic discovery fails but direct TCP communication works, use the manual IP option.

This should be documented as a network-environment limitation rather than an application failure.

---

# 39. Final Deliverables

Submit:

```text
lanshare/
├── main.py
├── sender.py
├── receiver.py
├── discovery.py
├── history.py
├── protocol.py
├── config.py
├── received/
└── README.md
```

Also include:

- Project report
- Architecture diagram
- Screenshots
- Test results
- Short explanation of syllabus concepts used

---

# 40. Viva / Evaluation Mapping

Be prepared to explain these questions.

## Why TCP for file transfer?

Because files require reliable and ordered delivery.

## Why UDP for discovery?

Discovery is a short broadcast-style operation where a persistent connection is unnecessary.

## Why `sendall()` instead of `send()`?

`sendall()` continues sending until all provided bytes have been passed to the socket or an error occurs.

## Why is `recv_exact()` needed?

TCP is a stream; a single `recv()` may return fewer bytes than requested.

## Why send file size first?

The receiver needs to know exactly how many bytes belong to the current file.

## Why read the file in chunks?

It avoids loading the entire file into memory.

## Why use threads?

The receiver must listen for incoming network connections while the main program remains responsive to terminal input.

## Why SQLite?

SQLite is lightweight, local, built into Python through `sqlite3`, and directly aligned with the database-processing portion of the syllabus.

## Why not use FTP directly?

FTP concepts are part of the syllabus, but the project can more directly demonstrate the socket-programming concepts taught in Session 9 by implementing the transfer channel itself. It remains a small educational file-transfer system rather than a full FTP implementation.

---

# 41. Syllabus Mapping Summary

| Project Component | ICS 214 Concept |
|---|---|
| Terminal menu | Input/output, conditions, loops |
| File path list | Lists |
| Receiver information | Dictionaries / tuples |
| File names and IPs | Strings |
| Modular code | Functions and modules |
| Sender / receiver classes | OOP |
| Reading and writing files | File processing |
| TCP communication | Socket programming |
| UDP discovery | Network programming |
| History | SQLite |
| Background receiver | Threading |
| Multiple connections | Multithreading |
| Binary transfer | File-transfer concepts |

---

# 42. Source Basis From Supplied Course Material

This plan is intentionally constrained to concepts present in the supplied ICS 214 material.

Relevant supplied sessions include:

- **Session 3** — File processing, including reading and writing files.
- **Session 8** — Classes and object-oriented programming.
- **Session 9** — Database processing, SQLite, network programming, sockets, TCP/UDP concepts, and client/server socket workflow.
- **Session 10** — FTP/file-transfer concepts and Python threading/multithreading.

In particular, Session 9 demonstrates the standard socket workflow involving `socket()`, `bind()`, `listen()`, `accept()`, `connect()`, `send()`, and `recv()`, while Session 10 explicitly discusses threads as useful for handling multiple client connections and concurrent operations.

---

# 43. Final Development Rule

Build in this exact order:

```text
TCP message
    ↓
Single file
    ↓
Reliable protocol framing
    ↓
Bulk files
    ↓
SQLite history
    ↓
Background receiving
    ↓
UDP discovery
    ↓
Terminal integration
    ↓
Error handling
    ↓
Testing
    ↓
Documentation
```

Do **not** start with the terminal UI or discovery system.

The first major technical goal should be:

> Transfer one arbitrary binary file correctly from Computer A to Computer B using TCP.

Once that works reliably, every remaining feature can be added incrementally.
