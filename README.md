# Secure Test Bed for Diffie-Hellman Key Exchange

This project is a small socket-based chat demo written in Python. It includes:

- `chat_insecure.py` for plaintext messaging
- `chat_secure.py` for a Diffie-Hellman key exchange followed by encrypted messaging
- `network_driver.py` as the provided networking layer
- `classes.py` for the serializable message types passed between peers
- `shift_cipher.py` for the shared-secret text transformation used by the secure demo

## How it works

### Insecure chat

The insecure version sends each message as plain text:

1. One terminal starts a listener.
2. A second terminal connects to it.
3. Messages are wrapped in a `Message` object and sent directly across the socket.

### Secure chat

The secure version adds a simple key-exchange flow before chatting:

1. The connecting side generates Diffie-Hellman parameters and sends a `DHInit` message.
2. The listening side replies with a `DHResp` message containing its public value.
3. Both sides compute the same shared secret independently.
4. Chat messages are wrapped in `SecureMessage` objects and transformed with the shared secret before sending.

This is a good learning demo, but it is not production-grade cryptography. The message protection step uses a printable-ASCII shift cipher based on the shared key, which is useful for illustrating the flow but should not be used for real secure messaging.

## Requirements

- Python 3.10+
- Two terminals

No third-party packages are required.

## Running the project

Open two terminals in the project folder.

### Plaintext demo

In terminal 1:

```bash
python chat_insecure.py listen 127.0.0.1 5000
```

In terminal 2:

```bash
python chat_insecure.py connect 127.0.0.1 5000
```

### Secure demo

In terminal 1:

```bash
python chat_secure.py listen 127.0.0.1 5001
```

In terminal 2:

```bash
python chat_secure.py connect 127.0.0.1 5001
```

Type messages in either terminal and press Enter to send. Type `exit` to close the client.

## Project structure

```text
.
|-- README.md
|-- chat_insecure.py
|-- chat_secure.py
|-- classes.py
|-- network_driver.py
`-- shift_cipher.py
```
