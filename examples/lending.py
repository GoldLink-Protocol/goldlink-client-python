'''
Example for lending.

Usage: python -m examples.lending
'''

import os
from web3 import Web3
from dotenv import load_dotenv

from goldlink import Client
from goldlink import constants

load_dotenv()

# Amount to lend.
LEND_AMOUNT = 80000000

# Load in ENVVAR
PUBLIC_KEY = os.getenv('TEST_OWNER_PUBLIC_KEY')
PRIVATE_KEY = os.getenv('TEST_OWNER_PRIVATE_KEY')

# Initialize client.
client = Client(
    network_id=constants.NETWORK_ID_FUJI,
    web3=Web3(Web3.HTTPProvider(constants.WEB_PROVIDER_URL_FUJI)),
    private_key=PRIVATE_KEY,
    strategy_reserve=constants.CONTRACTS[constants.RESERVE][constants.NETWORK_ID_FUJI]
)

# Get relevant contract addresses.
erc20 = client.reader.get_strategy_asset()

# Get some relevant "before" data points.
before_reserve_balance = client.reader.get_balance_of(erc20, client.strategy_reserve)
print("BEFORE: ", client.reader.get_balance_of(erc20, PUBLIC_KEY))

options = {
    'gasPrice': 25000000000
}

# Set approval for a strategy reserve to pull funds from this wallet.
print("Awaiting lending approval")
approve_transaction = client.writer.approve(
    address=client.strategy_reserve,
    amount=LEND_AMOUNT * 10,
    erc20=erc20,
    send_options=options
)
client.writer.wait_for_transaction(approve_transaction)
print("Lending approved")

# Lend to a strategy reserve.
print("Begin a deposit")
deposit_transaction = client.writer.deposit(
    amount=LEND_AMOUNT,
    on_behalf_of=PUBLIC_KEY,
    send_options=options
)
receipt = client.writer.wait_for_transaction(deposit_transaction)
depositEvent = client.event_handler.handle_deposit_event(
    client.strategy_reserve,
    receipt
)
print("Deposit Event: ", depositEvent)

# Lend to a strategy reserve via minting.
print("Begin a mint")
mint_transaction = client.writer.mint(
    shares=LEND_AMOUNT,
    on_behalf_of=PUBLIC_KEY,
    send_options=options
)
receipt = client.writer.wait_for_transaction(mint_transaction)
depositEvent = client.event_handler.handle_deposit_event(
    client.strategy_reserve,
    receipt
)
print("Mint Event: ", depositEvent)

# Withdraw from a strategy reserve via minting.
print("Begin a withdraw")
withdraw_transaction = client.writer.withdraw(
    amount=20000000,
    on_behalf_of=PUBLIC_KEY,
    send_options=options
)
receipt = client.writer.wait_for_transaction(withdraw_transaction)
depositEvent = client.event_handler.handle_withdraw_event(
    client.strategy_reserve,
    receipt
)
print("Withdraw Event: ", depositEvent)

# Redeem from a strategy reserve via minting.
print("Begin a redemption")
redeem_transaction = client.writer.redeem(
    shares=20000000,
    on_behalf_of=PUBLIC_KEY,
    send_options=options
)
receipt = client.writer.wait_for_transaction(redeem_transaction)
depositEvent = client.event_handler.handle_withdraw_event(
    client.strategy_reserve,
    receipt
)
print("Redeem Event: ", depositEvent)

# Verify lending succeeded.
after_reserve_balance = client.reader.get_balance_of(erc20, client.strategy_reserve)

# Print effects of lending.
print("Strategy Reserve balance: ", after_reserve_balance)
print("Lender balance: ", client.reader.get_balance_of(erc20, PUBLIC_KEY))
