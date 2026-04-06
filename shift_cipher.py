"""Simple printable-ASCII shift helpers used by the secure chat demo."""

PRINTABLE_ASCII_START = 32
PRINTABLE_ASCII_END = 126
PRINTABLE_ASCII_RANGE = PRINTABLE_ASCII_END - PRINTABLE_ASCII_START + 1


def encrypt(text: str, key: int) -> str:
    """Shift printable ASCII characters using the shared key."""
    output = []
    shift = key % PRINTABLE_ASCII_RANGE

    for char in text:
        code = ord(char)
        if PRINTABLE_ASCII_START <= code <= PRINTABLE_ASCII_END:
            normalized = code - PRINTABLE_ASCII_START
            output.append(
                chr((normalized + shift) % PRINTABLE_ASCII_RANGE + PRINTABLE_ASCII_START)
            )
        else:
            output.append(char)

    return "".join(output)


def decrypt(text: str, key: int) -> str:
    """Reverse the printable ASCII shift."""
    output = []
    shift = key % PRINTABLE_ASCII_RANGE

    for char in text:
        code = ord(char)
        if PRINTABLE_ASCII_START <= code <= PRINTABLE_ASCII_END:
            normalized = code - PRINTABLE_ASCII_START
            output.append(
                chr((normalized - shift) % PRINTABLE_ASCII_RANGE + PRINTABLE_ASCII_START)
            )
        else:
            output.append(char)

    return "".join(output)
