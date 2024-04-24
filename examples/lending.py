'''
Example for lending.

Usage: python -m examples.lending
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

# Amount to lend.
LEND_AMOUNT = 80000000

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
strategy_reserve = "0x3e3c1e5477f5F3261D7c25088566e548405B724B"
erc20 = client.reader.get_strategy_asset(strategy_reserve=strategy_reserve)

# Get some relevant "before" data points.
before_reserve_balance = client.reader.get_balance_of(erc20, strategy_reserve)
print("BEFORE: ", client.reader.get_balance_of(erc20, PUBLIC_KEY))

options = {
    'gasPrice': 1000000000
}

# Set approval for a strategy reserve to pull funds from this wallet.
print("Awaiting lending approval")
approve_transaction = client.writer.approve_address(
    address=strategy_reserve, 
    amount=LEND_AMOUNT * 10, 
    erc20=erc20,
    send_options=options
)
client.writer.wait_for_transaction(approve_transaction)
print("Lending approved")

# Lend to a strategy reserve.
print("Begin a deposit")
deposit_transaction = client.writer.deposit(
    LEND_AMOUNT,
    strategy_reserve,
    send_options=options
)
receipt = client.writer.wait_for_transaction(deposit_transaction)
depositEvent = client.event_handler.handle_deposit_event(
    strategy_reserve,
    receipt
)
print("Deposit Event: ", depositEvent)

# Lend to a strategy reserve via minting.
print("Begin a mint")
mint_transaction = client.writer.mint(
    shares=LEND_AMOUNT,
    strategy_reserve=strategy_reserve,
    send_options=options
)
receipt = client.writer.wait_for_transaction(mint_transaction)
depositEvent = client.event_handler.handle_deposit_event(
    strategy_reserve,
    receipt
)
print("Mint Event: ", depositEvent)

# Withdraw from a strategy reserve via minting.
print("Begin a withdraw")
withdraw_transaction = client.writer.withdraw(
    amount=20000000,
    strategy_reserve=strategy_reserve,
    send_options=options
)
receipt = client.writer.wait_for_transaction(withdraw_transaction)
depositEvent = client.event_handler.handle_withdraw_event(
    strategy_reserve,
    receipt
)
print("Withdraw Event: ", depositEvent)

# Redeem from a strategy reserve via minting.
print("Begin a redemption")
redeem_transaction = client.writer.redeem(
    shares=20000000,
    strategy_reserve=strategy_reserve,
    send_options=options
)
receipt = client.writer.wait_for_transaction(redeem_transaction)
depositEvent = client.event_handler.handle_withdraw_event(
    strategy_reserve,
    receipt
)
print("Redeem Event: ", depositEvent)

# Verify lending succeeded.
after_reserve_balance = client.reader.get_balance_of(erc20, strategy_reserve)

# Print effects of lending.
print("Strategy Reserve balance: ", after_reserve_balance)
print("Lender balance: ", client.reader.get_balance_of(erc20, PUBLIC_KEY))
