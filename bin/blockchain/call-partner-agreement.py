import argparse
import getpass
import json
import os

from axolpy import configuration, logging
from web3 import Web3


def init_arg_parser() -> argparse.ArgumentParser:
    """
    Initialize argument parser.

    :return: An argument parser for inputs.
    :rtype: :class:`argparse.ArgumentParser`
    """
    arg_parser = argparse.ArgumentParser(
        description="Call the Partner Agreement contract deployed on the chain.")
    arg_parser.add_argument("-k", "--private-key")
    arg_parser.add_argument("-a", "--contract-address", required=True)

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
contract_address: str = args.contract_address
# We use the local copy of abi
with open(f'{config["main"]["distribution.path"]}/PartnerAgreement.json', "r") as file:
    compiled_sol = json.load(file)
abi: str = compiled_sol["contracts"]["PartnerAgreement.sol"]["PartnerAgreement"]["abi"]

w3: Web3 = Web3(Web3.HTTPProvider(config["web3"]["http_provider"]))
chain_id: int = config["main"].getint("chain.id")
wallet_address: str = config["wallet"]["local.address.0"]
nonce = w3.eth.get_transaction_count(wallet_address)

logger.info(f"Wallet address is {wallet_address}")
logger.info(f"Call the contract at {contract_address}")
w3contract = w3.eth.contract(address=contract_address, abi=abi)

# Set the bank name
bankname_transaction = w3contract.functions.setBankName("A_FAKE_BANK").buildTransaction(
    {"chainId": chain_id, "from": wallet_address, "nonce": nonce})

signed_bankname_txn = w3.eth.account.sign_transaction(
    bankname_transaction, private_key)
logger.info("Updating Bank Name ...")
bankname_tx_hash = w3.eth.send_raw_transaction(
    transaction=signed_bankname_txn.rawTransaction)
logger.info("Waiting for bank name transaction receipt")
tx_receipt = w3.eth.wait_for_transaction_receipt(bankname_tx_hash)

logger.info(w3contract.functions.getBankName().call())
