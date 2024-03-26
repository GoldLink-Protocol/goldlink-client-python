'''
Example for withdawing native assets and ERC20. Only emits on withdraw ERC20 if assets are present in the strategy account.

Usage: python -m examples.withdrawals
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
PUBLIC_KEY = os.getenv('TEST_ACCOUNT_2_PUBLIC_KEY')
PRIVATE_KEY = os.getenv('TEST_ACCOUNT_2_PRIVATE_KEY')
STRATEGY_ACCOUNT = os.getenv('WITHDRAW_BALANCE_STRATEGY_ACCOUNT')

# Initialize client.
client = Client(
    network_id=NETWORK_ID_SEPOLIA,
    web3=Web3(Web3.HTTPProvider(WEB_PROVIDER_URL)),
    private_key=PRIVATE_KEY,
    default_address=PUBLIC_KEY,
)

options = {
    'gasPrice': 1000000000
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
    tokens=["0x773330693cb7d5D233348E25809770A32483A940"],
    amounts=[1000],
    send_options=options
)
receipt = client.writer.wait_for_transaction(borrow_erc20_transaction)
print("Withdraw erc20, event: ", client.event_handler.handle_withdraw_erc20_assets_event(STRATEGY_ACCOUNT, receipt))
