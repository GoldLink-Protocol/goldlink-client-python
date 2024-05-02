'''
Example for borrowing. Additionally, only works if
a lending position had been created.
Use `python -m examples.lending` to create a lending position.

Usage: python -m examples.borrowing
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

bank = constants.CONTRACTS[constants.BANK][constants.NETWORK_ID_FUJI]

# Initialize client.
client = Client(
    network_id=constants.NETWORK_ID_FUJI,
    web3=Web3(Web3.HTTPProvider(constants.WEB_PROVIDER_URL_FUJI)),
    private_key=PRIVATE_KEY,
    strategy_bank=bank,
)

# Get relevant contract addresses.
erc20 = client.reader.get_strategy_asset()

options = {
    'gasPrice': 25000000000
}

print(
    f"All strategy accounts: {client.reader.get_strategy_accounts_for_bank()}",
)
print(
    f"Owned strategy accounts: {client.reader.get_strategy_accounts_for_bank(PUBLIC_KEY)}",
)

print(f"Deploying strategy account for strategy bank {client.strategy_bank}")
open_transaction = client.writer.open_account(
    on_behalf_of=PUBLIC_KEY,
    send_options=options
)
receipt = client.writer.wait_for_transaction(open_transaction)
openAccountEvent = client.event_handler.handle_open_account_event(
    client.strategy_bank,
    receipt
)
strategy_account = openAccountEvent["strategyAccount"]
client.strategy_account = strategy_account
print(f"Strategy account deployed, address {strategy_account}")

# Set approval for strategy account to pull funds from this wallet.
print(f"Approve strategy account {strategy_account} to pull collateral")
approve_transaction = client.writer.approve(
    address=client.strategy_bank,
    amount=BORROW_AMOUNT * 10,
    erc20=erc20,
    send_options=options
)
client.writer.wait_for_transaction(approve_transaction)
print("Add collateral approved")

print(f"Adding collateral to strategy account {strategy_account}")
add_collateral_transaction = client.writer.add_collateral(
    amount=COLLATERAL_AMOUNT,
    send_options=options
)
receipt = client.writer.wait_for_transaction(add_collateral_transaction)
print(
    "Collateral added, event: ",
    client.event_handler.handle_add_collateral_event(client.strategy_bank, receipt),
)

# Create borrow balance.
print("Borrowing into strategy account")
borrow_transaction = client.writer.borrow(
    BORROW_AMOUNT,
    send_options=options
)
receipt = client.writer.wait_for_transaction(borrow_transaction)
borrow_event = client.event_handler.handle_borrow_event(client.strategy_bank, receipt)
print("Strategy account borrowed, event: ", borrow_event)

strategy_reserve = client.reader.get_strategy_reserve_for_bank()

# Print effects of borrowing.
print("Reserve balance: ", client.reader.get_balance_of(erc20, strategy_reserve))
print("Strategy Bank balance: ", client.reader.get_balance_of(erc20, client.strategy_bank))
print("Strategy Account balance: ", client.reader.get_balance_of(erc20, strategy_account))
print("Borrower balance: ", client.reader.get_balance_of(erc20, PUBLIC_KEY))

# Repay borrow balance.
print(f"Repaying from strategy account {strategy_account}")
repay_transaction = client.writer.repay(
    BORROW_AMOUNT,
    send_options=options
)
receipt = client.writer.wait_for_transaction(repay_transaction)
repay_event = client.event_handler.handle_repay_event(client.strategy_bank, receipt)
print("Strategy account repaid, event: ", repay_event)

# Get the strategy account balance.
strategy_account_balance = client.reader.get_strategy_account_holdings(strategy_account)

# Withdraw collateral.
print(f"Withdrawing collateral from strategy account {strategy_account}")
withdraw_transaction = client.writer.withdraw_collateral(
    strategy_account_balance["collateral"],
    on_behalf_of=PUBLIC_KEY,
    send_options=options
)
receipt = client.writer.wait_for_transaction(withdraw_transaction)
withdraw_collateral_event = client.event_handler.handle_withdraw_collateral_event(client.strategy_bank, receipt)
print("Collateral withdrawn, event: ", withdraw_collateral_event)
