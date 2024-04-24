'''
Example for liquidating a strategy account. Reverts if account is not liquidatable.

Usage: python -m examples.liquidation
'''

import os
from web3 import Web3
from dotenv import load_dotenv

from goldlink import Client
from goldlink.constants import NETWORK_ID_SEPOLIA

from examples.constants import WEB_PROVIDER_URL

## Sepolia Contracts
## Controller: https://sepolia.arbiscan.io/address/0x40A633EeF249F21D95C8803b7144f19AAfeEF7ae
## Mock ERC20: https://sepolia.arbiscan.io/address/0x773330693cb7d5D233348E25809770A32483A940
## Bank: https://sepolia.arbiscan.io/address/0xD4324a5f29147688fB4ca959e901b0Ff50Bd8e3a
## Reserve: https://sepolia.arbiscan.io/address/0x3e3c1e5477f5F3261D7c25088566e548405B724B

load_dotenv()

# Load in ENVVAR
PUBLIC_KEY = os.getenv('TEST_ACCOUNT_3_PUBLIC_KEY')
PRIVATE_KEY = os.getenv('TEST_ACCOUNT_3_PRIVATE_KEY')
STRATEGY_ACCOUNT = os.getenv('LIQUIDATABLE_STRATEGY_ACCOUNT')

# Initialize client.
client = Client(
    network_id=NETWORK_ID_SEPOLIA,
    web3=Web3(Web3.HTTPProvider(WEB_PROVIDER_URL)),
    private_key=PRIVATE_KEY,
    default_address=PUBLIC_KEY,
)

# Get relevant contract addresses.
strategy_bank = "0xD4324a5f29147688fB4ca959e901b0Ff50Bd8e3a"

options = {
    'gasPrice': 1000000000
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
