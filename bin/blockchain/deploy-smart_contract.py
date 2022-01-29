import argparse
import getpass
import json
import os
import subprocess
import sys

from axolpy import configuration, logging, solidity
from web3 import Web3


def init_arg_parser() -> argparse.ArgumentParser:
    """
    Initialize argument parser.

    :return: An argument parser for inputs.
    :rtype: :class:`argparse.ArgumentParser`
    """
    arg_parser = argparse.ArgumentParser(
        description="Deploy smart contract to Ethereum.")
    arg_parser.add_argument("-k", "--private-key")
    arg_parser.add_argument("-c", "--contract-name", required=True)
    arg_parser.add_argument("--solidity-compiler-version")

    return arg_parser


arg_parser = init_arg_parser()
args = arg_parser.parse_args()

logger = logging.get_logger(name=os.path.basename(__file__))
logging.set_level(logging.INFO)
logging.show_milliseconds()

config = configuration.AxolpyConfigManager.get_context(name="blockchain")
base_path = config["main"]["base_path"]

private_key: str = args.private_key if args.private_key else getpass.getpass(
    prompt="Private Key: ")
contract_name: str = args.contract_name
contract_filepath: str = f'{config["main"]["contracts.path"]}/{contract_name}.sol'
solidity_compiler_version: str = args.solidity_compiler_version \
    if args.solidity_compiler_version \
    else config["main"]["solidity.compiler.version"]

contract_content: str = None

logger.info(f"Reading contract file {contract_filepath}")
with open(contract_filepath, "r") as file:
    contract_content = file.read()

compiled_sol = solidity.SolidityHelper.solcx_compile_standard(
    source_name=f"{contract_name}.sol",
    source_content=contract_content,
    solidity_compiler_version=solidity_compiler_version)

with open(f'{config["main"]["distribution.path"]}/{contract_name}.json', "w") as file:
    json.dump(compiled_sol, file)

# Get bytecode and abi from compiled solidity file
bytecode: str = compiled_sol["contracts"][f"{contract_name}.sol"][contract_name]["evm"]["bytecode"]["object"]
abi: str = compiled_sol["contracts"][f"{contract_name}.sol"][contract_name]["abi"]

# Connect to the provider
w3: Web3 = Web3(Web3.HTTPProvider(config["web3"]["http_provider"]))
chain_id: int = config["main"].getint("chain.id")
wallet_address: str = config["wallet"]["local.address.0"]
nonce = w3.eth.get_transaction_count(wallet_address)

w3contract = w3.eth.contract(abi=abi, bytecode=bytecode)

logger.info(f"Wallet address is {wallet_address}")
contract_txn = w3contract.constructor().buildTransaction(
    {"chainId": chain_id, "from": wallet_address, "nonce": nonce})

# Sign the transaction and send it to the network
signed_contract_txn = w3.eth.account.sign_transaction(
    contract_txn, private_key)
logger.info("Deploying contract ...")
tx_hash = w3.eth.send_raw_transaction(
    transaction=signed_contract_txn.rawTransaction)
logger.info("Waiting for transaction receipt ...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
logger.info(f"Contract is deployed to {tx_receipt.contractAddress}")

# Run the corresponding script we built for trial run
with subprocess.Popen([sys.executable,
                       f"{base_path}/bin/blockchain/call-partner-agreement.py",
                       "--contract-address",
                       tx_receipt.contractAddress],
                      stdout=subprocess.PIPE,
                      stderr=subprocess.STDOUT) as proc:
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        print(line.decode("utf-8").rstrip())
    proc.stdout.close()
