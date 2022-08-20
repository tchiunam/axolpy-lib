from prompt_toolkit.document import Document
from prompt_toolkit.validation import ValidationError, Validator


class NumberValidator(Validator):
    """
    A validator that validates if input is a number.
    """

    def validate(self, document: Document) -> None:
        """
        Validate if input is a number.

        :param document: Input from the prompt.
        :type document: :class:`prompt_toolkit.document.Document`

        :raises: :class:`ValidationError` if input is not a number.
        """

        text = document.text

        if text and not text.isdigit():
            i = 0

            # Get index of first non numeric character
            # and move the cursor there.
            for i, c in enumerate(text):
                if not c.isdigit():
                    break

            raise ValidationError(message="Only number is allowed.",
                                  cursor_position=i)


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
