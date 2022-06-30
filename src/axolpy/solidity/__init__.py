import solcx


class SolidityHelper():
    def __init__(self, *args, **kwargs):
        """
        Helper class for solidity handling.
        """

    @staticmethod
    def solcx_compile_standard(source_name: str, source_content: str, solidity_compiler_version: str) -> str:
        """
        Compile Solidity contracts using the JSON-input-output interface.

        :param source_name: Source name.
        :type source_name: str
        :param source_content: Source content.
        :type source_content: str
        :param solidity_compiler_version: Soidity compiler's version.
        :type solidity_compiler_version: str

        :return: Compiler JSON output.
        :rtype: str
        """

        return solcx.compile_standard(
            {
                "language": "Solidity",
                "sources": {source_name: {"content": source_content}},
                "settings": {
                    "outputSelection": {
                        "*": {
                            "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                        }
                    }
                }
            },
            solc_version=solidity_compiler_version
        )
