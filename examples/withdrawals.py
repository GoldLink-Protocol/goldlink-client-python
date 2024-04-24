'''
Example for withdawing native assets and ERC20. Only emits on withdraw ERC20 if assets are present in the strategy account.

Usage: python -m examples.withdrawals
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
PUBLIC_KEY = os.getenv('TEST_ACCOUNT_2_PUBLIC_KEY')
PRIVATE_KEY = os.getenv('TEST_ACCOUNT_2_PRIVATE_KEY')
STRATEGY_ACCOUNT = os.getenv('WITHDRAW_BALANCE_STRATEGY_ACCOUNT')

# Initialize client.
client = Client(
    network_id=NETWORK_ID_FUJI,
    web3=Web3(Web3.HTTPProvider(WEB_PROVIDER_URL)),
    private_key=PRIVATE_KEY,
    default_address=PUBLIC_KEY,
)

options = {
    'gasPrice': 25000000000
}

print(f"Withdrawing native asset from strategy account {STRATEGY_ACCOUNT}")
borrow_native_transaction = client.writer.withdraw_native_asset(
    strategy_account=STRATEGY_ACCOUNT,
    amount=0,
    send_options=options
)
receipt = client.writer.wait_for_transaction(borrow_native_transaction)
print("Withdraw native, event: ", client.event_handler.handle_withdraw_native_asset_event(STRATEGY_ACCOUNT, receipt))

print(f"Withdrawing ERC20 from strategy account {STRATEGY_ACCOUNT}")
borrow_erc20_transaction = client.writer.withdraw_erc20_assets(
    strategy_account=STRATEGY_ACCOUNT,
    tokens=["0x82F0b3695Ed2324e55bbD9A9554cB4192EC3a514"],
    amounts=[1000],
    send_options=options
)
receipt = client.writer.wait_for_transaction(borrow_erc20_transaction)
print("Withdraw erc20, event: ", client.event_handler.handle_withdraw_erc20_assets_event(STRATEGY_ACCOUNT, receipt))
