"""Baseline plaintext chat client."""

import sys

from classes import Message
from network_driver import NetworkDriver


def receive_message(msg: Message) -> None:
    print(f"> {msg.text}")


def send_message(driver: NetworkDriver, text: str) -> None:
    driver.send(Message(text))


def main() -> None:
    if len(sys.argv) != 4:
        print("Usage: python chat_insecure.py [listen|connect] [host] [port]")
        return

    mode, host, port = sys.argv[1], sys.argv[2], int(sys.argv[3])
    driver = NetworkDriver(mode, host, port, on_message=receive_message)
    driver.start()

    try:
        while True:
            text = input()
            if text.strip().lower() == "exit":
                break
            send_message(driver, text)
    except KeyboardInterrupt:
        print("\nExiting.")
    finally:
        driver.close()


if __name__ == "__main__":
    main()
