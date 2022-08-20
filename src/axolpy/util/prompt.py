from prompt_toolkit.document import Document
from prompt_toolkit.validation import ValidationError, Validator


class CryptographyKeyValidator(Validator):
    """
    A validator that validates if input is a cryptography key.
    """

    def validate(self, document: Document) -> None:
        """
        Validate if input is a cryptography key.

        :param document: Input from the prompt.
        :type document: :class:`prompt_toolkit.document.Document`

        :raises: :class:`ValidationError` if input is not a cryptography key.
        """

        text = document.text

        if text and len(text) != 44:
            raise ValidationError(message="Cryptography key must be 44 characters long.",
                                  cursor_position=len(text))
