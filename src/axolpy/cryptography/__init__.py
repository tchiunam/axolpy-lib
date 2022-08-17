from pathlib import Path

from cryptography.fernet import Fernet


def generate_key() -> bytes:
    """
    Generate a cryptography key.

    :return: Key.
    :rtype: bytes
    """

    return Fernet.generate_key()


def generate_key_file(path: Path = None) -> Path:
    """
    Generate a key and save it to the given path.

    :param path: Path to save key file. If None, the key will be saved to the
        current working directory.
    :type path: Path

    :return: Path to the key file.
    :rtype: Path
    """

    key_file_path = path / "secret.key" if path else Path.cwd() / "secret.key"
    if key_file_path.exists():
        raise FileExistsError("secret.key file already exists.")
    with key_file_path.open("wb") as key_file:
        key_file.write(generate_key())

    return key_file_path


def load_key(key_file_path: Path) -> bytes:
    """
    Load the key.

    :param key_file_path: Path to the key file.
    :type key_file_path: Path

    :return: Key.
    :rtype: bytes
    """

    return key_file_path.open("rb").read()


def encrypt_message(message: str, key: bytes | Path) -> bytes:
    """
    Encrypt a message.

    :param message: Message to encrypt.
    :type message: str
    :param key: Key to use for encryption.
    :type key: bytes | Path

    :return: Encrypted message.
    :rtype: bytes
    """

    encoded_message = message.encode()

    if isinstance(key, Path):
        key = load_key(key)
    f = Fernet(key)
    return f.encrypt(data=encoded_message)


def decrypt_message(encrypted_message: bytes | str, key: bytes | Path) -> bytes:
    """
    Decrypt an encrypted message.

    :param encrypted_message: Encrypted message to decrypt.
    :type encrypted_message: bytes | str
    :param key: Key to use for decryption.
    :type key: bytes | Path

    :return: Decrypted message.
    :rtype: bytes
    """

    if isinstance(key, Path):
        key = load_key(key)
    f = Fernet(key)
    return f.decrypt(token=encrypted_message.encode()
                     if isinstance(encrypted_message, str) else encrypted_message)
