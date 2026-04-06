"""Secure chat demo using Diffie-Hellman and a shared-secret shift cipher."""

import random
import sys
import time

from classes import DHInit, DHResp, SecureMessage
from network_driver import NetworkDriver
from shift_cipher import decrypt, encrypt

driver = None
shared_key = None
_client_p = None
_client_a = None


def is_prime(n: int, rounds: int = 8) -> bool:
    """Run a Miller-Rabin primality check."""
    if n in (2, 3):
        return True
    if n < 2 or n % 2 == 0:
        return False

    s = 0
    d = n - 1
    while d % 2 == 0:
        d //= 2
        s += 1

    for _ in range(rounds):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def generate_safe_prime(bits: int = 512) -> tuple[int, int]:
    """Generate a safe prime p = 2q + 1 and return both p and q."""
    while True:
        q = random.getrandbits(bits - 1) | (1 << (bits - 2)) | 1
        if not is_prime(q):
            continue

        p = 2 * q + 1
        if is_prime(p):
            return p, q


def find_generator(p: int, q: int) -> int:
    """Find a generator for the subgroup of order q modulo p."""
    while True:
        g = random.randrange(2, p - 1)
        if pow(g, 2, p) != 1 and pow(g, q, p) != 1:
            return g


def receive_message(msg) -> None:
    global shared_key

    if isinstance(msg, DHInit):
        print("Received Diffie-Hellman parameters from peer.")
        p, g, peer_public = msg.p, msg.g, msg.public
        private_value = random.randrange(2, p - 1)
        public_value = pow(g, private_value, p)
        driver.send(DHResp(public_value))
        shared_key = pow(peer_public, private_value, p)
        print("Shared secret established.")
        return

    if isinstance(msg, DHResp):
        print("Received Diffie-Hellman response from peer.")
        shared_key = pow(msg.public, _client_a, _client_p)
        print("Shared secret established.")
        return

    if isinstance(msg, SecureMessage):
        if shared_key is None:
            print("Received encrypted message before key exchange; ignoring.")
            return

        plaintext = decrypt(msg.ciphertext, shared_key)
        print(f"\nPeer: {plaintext}")
        return

    print("Received unexpected message type.")


def send_message(driver: NetworkDriver, text: str) -> None:
    ciphertext = encrypt(text, shared_key)
    driver.send(SecureMessage(ciphertext))


def main() -> None:
    global driver, _client_p, _client_a

    if len(sys.argv) != 4:
        print("Usage: python chat_secure.py [listen|connect] [host] [port]")
        return

    mode, host, port = sys.argv[1], sys.argv[2], int(sys.argv[3])
    driver = NetworkDriver(mode, host, port, on_message=receive_message)
    driver.start()

    if mode == "connect":
        _client_p, q = generate_safe_prime(bits=512)
        generator = find_generator(_client_p, q)
        _client_a = random.randrange(2, _client_p - 1)
        public_value = pow(generator, _client_a, _client_p)
        driver.send(DHInit(_client_p, generator, public_value))

    try:
        while shared_key is None:
            time.sleep(0.05)

        while True:
            text = input("You: ")
            if text.strip().lower() == "exit":
                break
            send_message(driver, text)
    except KeyboardInterrupt:
        print("\nExiting.")
    finally:
        driver.close()


if __name__ == "__main__":
    main()
