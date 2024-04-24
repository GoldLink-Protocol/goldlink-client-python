'''
Example for liquidating a strategy account. Reverts if account is not liquidatable.

Usage: python -m examples.liquidation
'''

import os
from web3 import Web3
from dotenv import load_dotenv

from goldlink import Client
from goldlink.constants import NETWORK_ID_FUJI

from examples.constants import WEB_PROVIDER_URL

## Fuji Contracts
## Controller: https://testnet.snowtrace.io/address/0xD70e13Ad0C3ba99c09a6130602C30Aac0dF41dA9
## ERC20: https://testnet.snowtrace.io/address/0x3eBDeaA0DB3FfDe96E7a0DBBAFEC961FC50F725F
## Bank: https://testnet.snowtrace.io/address/0x7D42836DB1CfAd7898B486B9C8265cE8d9c99D71
## Reserve: https://testnet.snowtrace.io/address/0x6513dDFE61AE59308B8E3D9483Da4579B3477Ff9

load_dotenv()

# Load in ENVVAR
PUBLIC_KEY = os.getenv('TEST_ACCOUNT_3_PUBLIC_KEY')
PRIVATE_KEY = os.getenv('TEST_ACCOUNT_3_PRIVATE_KEY')
STRATEGY_ACCOUNT = os.getenv('LIQUIDATABLE_STRATEGY_ACCOUNT')

# Initialize client.
client = Client(
    network_id=NETWORK_ID_FUJI,
    web3=Web3(Web3.HTTPProvider(WEB_PROVIDER_URL)),
    private_key=PRIVATE_KEY,
    default_address=PUBLIC_KEY,
)

# Get relevant contract addresses.
strategy_bank = "0x7D42836DB1CfAd7898B486B9C8265cE8d9c99D71"

options = {
    'gasPrice': 25000000000
}

print(f"Initiating liquidation for strategy account {STRATEGY_ACCOUNT}")
initiate_liquidation_transaction = client.writer.initiate_liquidation(
    strategy_account=STRATEGY_ACCOUNT,
    send_options=options
)
receipt = client.writer.wait_for_transaction(initiate_liquidation_transaction)
print("Initiate liquidation, event: ", client.event_handler.handle_initiate_liquidation_event(STRATEGY_ACCOUNT, receipt))

print(f"Processing liquidation for strategy account {STRATEGY_ACCOUNT}")
process_liquidation_transaction = client.writer.process_liquidation(
    strategy_account=STRATEGY_ACCOUNT,
    send_options=options
)
receipt = client.writer.wait_for_transaction(process_liquidation_transaction)
print("Process liquidation, event: ", client.event_handler.handle_process_liquidation_event(STRATEGY_ACCOUNT, receipt))
print("Liquidate loan, event: ", client.event_handler.handle_liquidate_loan_event(strategy_bank, receipt))
