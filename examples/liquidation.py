'''
Example for liquidating a strategy account. Reverts if account is not liquidatable.

Usage: python -m examples.liquidation
'''

import os
from web3 import Web3
from dotenv import load_dotenv

from goldlink import Client
from goldlink import constants

load_dotenv()

# Load in ENVVAR
PUBLIC_KEY = os.getenv('TEST_ACCOUNT_3_PUBLIC_KEY')
PRIVATE_KEY = os.getenv('TEST_ACCOUNT_3_PRIVATE_KEY')
STRATEGY_ACCOUNT = os.getenv('LIQUIDATABLE_STRATEGY_ACCOUNT')

# Initialize client.
client = Client(
    network_id=constants.NETWORK_ID_FUJI,
    web3=Web3(Web3.HTTPProvider(constants.WEB_PROVIDER_URL_FUJI)),
    private_key=PRIVATE_KEY,
    strategy_bank=constants.CONTRACTS[constants.BANK][constants.NETWORK_ID_FUJI],
)

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
print("Liquidate loan, event: ", client.event_handler.handle_liquidate_loan_event(client.strategy_bank, receipt))
