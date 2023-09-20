'''
Example for withdawing native assets and ERC20. Only emits on withdraw ERC20 if assets are present in the strategy account.

Usage: python -m examples.withdrawals
'''

import os
from web3 import Web3
from dotenv import load_dotenv

from goldlink import Client
from goldlink import constants

load_dotenv()

# Load in ENVVAR
PUBLIC_KEY = os.getenv('TEST_ACCOUNT_2_PUBLIC_KEY')
PRIVATE_KEY = os.getenv('TEST_ACCOUNT_2_PRIVATE_KEY')
STRATEGY_ACCOUNT = os.getenv('WITHDRAW_BALANCE_STRATEGY_ACCOUNT')

# Initialize client.
client = Client(
    network_id=constants.NETWORK_ID_FUJI,
    web3=Web3(Web3.HTTPProvider(constants.WEB_PROVIDER_URL_FUJI)),
    private_key=PRIVATE_KEY,
    strategy_bank=constants.CONTRACTS[constants.BANK][constants.NETWORK_ID_FUJI],
    strategy_account=STRATEGY_ACCOUNT,
)

options = {
    'gasPrice': 25000000000
}

print(f"Withdrawing native asset from strategy account {STRATEGY_ACCOUNT}")
borrow_native_transaction = client.writer.withdraw_native_asset(
    amount=0,
    on_behalf_of=PUBLIC_KEY,
    send_options=options
)
receipt = client.writer.wait_for_transaction(borrow_native_transaction)
print("Withdraw native, event: ", client.event_handler.handle_withdraw_native_asset_event(STRATEGY_ACCOUNT, receipt))

print(f"Withdrawing ERC20 from strategy account {STRATEGY_ACCOUNT}")
borrow_erc20_transaction = client.writer.withdraw_erc20_assets(
    tokens=["0x82F0b3695Ed2324e55bbD9A9554cB4192EC3a514"],
    amounts=[1000],
    on_behalf_of=PUBLIC_KEY,
    send_options=options
)
receipt = client.writer.wait_for_transaction(borrow_erc20_transaction)
print("Withdraw erc20, event: ", client.event_handler.handle_withdraw_erc20_assets_event(STRATEGY_ACCOUNT, receipt))
