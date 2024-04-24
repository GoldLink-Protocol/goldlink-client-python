'''
Example for borrowing. Additionally, only works if
a lending position had been created. Use `python -m examples.lending` to create a 
lending position on Fuji.

Usage: python -m examples.strategies.gmx_frf.manage_position
'''

import os
from web3 import Web3
from dotenv import load_dotenv

from goldlink import Client
from goldlink import constants

load_dotenv()

# Amount to borrow.
BORROW_AMOUNT = 15000000

# Amount of collateral
COLLATERAL_AMOUNT = 10000000

# Load in ENVVAR
PUBLIC_KEY = os.getenv('TEST_OWNER_PUBLIC_KEY')
PRIVATE_KEY = os.getenv('TEST_OWNER_PRIVATE_KEY')

# Market
GMX_MARKET="0xD996ff47A1F763E1e55415BC4437c59292D1F415"

# Initialize client.
client = Client(
    network_id=constants.NETWORK_ID_FUJI,
    web3=Web3(Web3.HTTPProvider(constants.WEB_PROVIDER_URL_FUJI)),
    private_key=PRIVATE_KEY,
    default_address=PUBLIC_KEY,
)

# Get relevant contract addresses.
strategy_bank = constants.CONTRACTS[constants.BANK][constants.NETWORK_ID_FUJI]
erc20 = client.reader.get_strategy_asset(strategy_bank=strategy_bank)

options = {
    'gasPrice': 25000000000
}

print(f"Deploying strategy account for strategy bank {strategy_bank}")
open_transaction = client.writer.open_account(
    strategy_bank=strategy_bank, 
    send_options=options
)
receipt = client.writer.wait_for_transaction(open_transaction)
openAccountEvent = client.event_handler.handle_open_account_event(
    strategy_bank,
    receipt
)
strategy_account = openAccountEvent["strategyAccount"]
print(f"Strategy account deployed, address {strategy_account}")

# Set approval for strategy account to pull funds from this wallet.
print(f"Approve strategy account {strategy_account} to pull collateral")
approve_transaction = client.writer.approve_address(
    address=strategy_bank, 
    amount=BORROW_AMOUNT * 10, 
    erc20=erc20,
    send_options=options
)
client.writer.wait_for_transaction(approve_transaction)
print("Add collateral approved")

print(f"Adding collateral to strategy account {strategy_account}")
add_collateral_transaction = client.writer.add_collateral(
    strategy_account=strategy_account,
    amount=COLLATERAL_AMOUNT,
    send_options=options
)
receipt = client.writer.wait_for_transaction(add_collateral_transaction)
print("Collateral added, event: ", client.event_handler.handle_add_collateral_event(strategy_bank, receipt))

# Create borrow balance.
print("Borrowing into strategy account")
borrow_transaction = client.writer.borrow(
    strategy_account,
    BORROW_AMOUNT,
    send_options=options
)
receipt = client.writer.wait_for_transaction(borrow_transaction)
borrow_event = client.event_handler.handle_borrow_event(strategy_bank, receipt)
print("Strategy account borrowed, event: ", borrow_event)

# Create position.
print("Creating GMX Market position")
open_position_transaction = client.gmx_frf_writer.create_increase_order(
    strategy_account=strategy_account,
    market=GMX_MARKET,
    amount=10000,
    execution_fee=100000,
    send_options=options
)
receipt = client.gmx_frf_writer.wait_for_transaction(open_position_transaction)
print("Create increase order event: ", client.gmx_frf_event_handler.handle_create_increase_order_event(strategy_account, receipt))

# TODO finish
