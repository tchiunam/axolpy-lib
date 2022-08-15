from pathlib import Path

import pytest
from axolpy.cryptography import (decrypt_message, encrypt_message,
                                 generate_key, load_key)


class TestEncryptDecryptMessage(object):
    """"
    Test encrypting and decrypting message.
    """

    _testdata_path = Path(__file__).parent.joinpath("testdata")
    _test_key_file_path = _testdata_path / "secret-test.key"

    def test_generate_key(self) -> None:
        """
        Test to generate a key.
        """

        key_file_path = generate_key(path=self._testdata_path)
        assert key_file_path.exists()
        assert key_file_path.is_file()

        try:
            with key_file_path.open("r") as key_file:
                assert len(key_file.read()) == 44

            with pytest.raises(FileExistsError):
                generate_key(path=self._testdata_path)
        finally:
            key_file_path.unlink()

    def test_load_key(self) -> None:
        """
        Test to load a key.
        """

        key = load_key(self._test_key_file_path)
        assert key.decode() == "jT1mItGMn4Dl5jp9Iz8IhIC_cSQyeTIf0W-5vKBSgg8="

    def test_encrypt_message(self) -> None:
        """
        Test to encrypt message with a key.
        """

        assert len(encrypt_message(
            message="I was born in the year of the fox.",
            key=self._test_key_file_path)) == 140

    def test_decrypt_message(self) -> None:
        """
        Test to decrypt message with a key.
        """

        assert decrypt_message(
            encrypted_message=encrypt_message(
                message="I was born in the year of the fox.",
                key=self._test_key_file_path),
            key=self._test_key_file_path).decode() == "I was born in the year of the fox."
