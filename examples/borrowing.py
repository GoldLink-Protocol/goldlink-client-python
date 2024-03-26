'''
Example for borrowing. Additionally, only works if
a lending position had been created. Use `python -m examples.lending` to create a 
lending position.

Usage: python -m examples.borrowing
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

# Amount to borrow.
BORROW_AMOUNT = 15000000

# Amount of collateral
COLLATERAL_AMOUNT = 10000000

# Load in ENVVAR
PUBLIC_KEY = os.getenv('TEST_OWNER_PUBLIC_KEY')
PRIVATE_KEY = os.getenv('TEST_OWNER_PRIVATE_KEY')

# Initialize client.
client = Client(
    network_id=NETWORK_ID_SEPOLIA,
    web3=Web3(Web3.HTTPProvider(WEB_PROVIDER_URL)),
    private_key=PRIVATE_KEY,
    default_address=PUBLIC_KEY,
)

# Get relevant contract addresses.
strategy_bank = "0xD4324a5f29147688fB4ca959e901b0Ff50Bd8e3a"
erc20 = client.reader.get_strategy_asset(strategy_bank=strategy_bank)

options = {
    'gasPrice': 1000000000
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

strategy_reserve = client.reader.get_strategy_reserve_for_bank(strategy_bank=strategy_bank)

# Print effects of borrowing.
print("Reserve balance: ", client.reader.get_balance_of(erc20, strategy_reserve))
print("Strategy Bank balance: ", client.reader.get_balance_of(erc20, strategy_bank))
print("Strategy Account balance: ", client.reader.get_balance_of(erc20, strategy_account))
print("Borrower balance: ", client.reader.get_balance_of(erc20, PUBLIC_KEY))

# Repay borrow balance.
print(f"Repaying from strategy account {strategy_account}")
repay_transaction = client.writer.repay(
    strategy_account,
    BORROW_AMOUNT,
    send_options=options
)
receipt = client.writer.wait_for_transaction(repay_transaction)
repay_event = client.event_handler.handle_repay_event(strategy_bank, receipt)
print("Strategy account repaid, event: ", repay_event)

# Get the strategy account balance.
strategy_account_balance = client.reader.get_strategy_account_holdings(strategy_bank, strategy_account)

# Withdraw collateral.
print(f"Withdrawing collateral from strategy account {strategy_account}")
withdraw_transaction = client.writer.withdraw_collateral(
    strategy_account,
    strategy_account_balance["collateral"],
    send_options=options
)
receipt = client.writer.wait_for_transaction(withdraw_transaction)
withdraw_collateral_event = client.event_handler.handle_withdraw_collateral_event(strategy_bank, receipt)
print("Collateral withdrawn, event: ", withdraw_collateral_event)
