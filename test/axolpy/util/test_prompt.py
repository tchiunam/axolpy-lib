import pytest
from axolpy.util.prompt import CryptographyKeyValidator, NumberValidator
from prompt_toolkit.document import Document
from prompt_toolkit.validation import ValidationError


def test_number_validator() -> None:
    """
    Test to run prompt validator to validate if input is a number.
    """

    validator = NumberValidator()

    assert validator.validate(document=Document(text="123456")) is None
    with pytest.raises(ValidationError):
        assert validator.validate(document=Document(text="1.1"))
    with pytest.raises(ValidationError):
        validator.validate(document=Document(text="abc"))


def test_cryptography_key_validator() -> None:
    """
    Test to run prompt validator to validate if input is a cryptography key file.
    """

    validator = CryptographyKeyValidator()

    assert validator.validate(document=Document(
        text="TLo07k-Wd-dJPxR3AvKsuE5-B9jRamZ6Pbq71c8UKJQ=")) is None
    with pytest.raises(ValidationError):
        validator.validate(document=Document(text="0123456789abcdefg"))
