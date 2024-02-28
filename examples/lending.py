'''
Example for lending. Assumes anvil is running.

Usage: python -m examples.lending
'''

from web3 import Web3
from goldlink import Client
from goldlink.constants import NETWORK_ID_ANVIL
from examples.constants import WEB_PROVIDER_URL, ETHEREUM_ADDRESS, ETHEREUM_PRIVATE_KEY

# Amount to lend.
LEND_AMOUNT = 40000000

# Initialize client.
client = Client(
    network_id=NETWORK_ID_ANVIL,
    web3=Web3(Web3.HTTPProvider(WEB_PROVIDER_URL)),
    private_key=ETHEREUM_PRIVATE_KEY,
    default_address=ETHEREUM_ADDRESS,
)

# Get relevant contract addresses.
strategy_reserve = "0xd8058efe0198ae9dD7D563e1b4938Dcbc86A1F81"
erc20 = client.reader.get_strategy_asset(strategy_reserve=strategy_reserve)

# Get some relevant "before" data points.
before_reserve_balance = client.reader.get_balance_of(erc20, strategy_reserve)
print("BEFORE: ", client.reader.get_balance_of(erc20, ETHEREUM_ADDRESS))

# Set approval for a strategy reserve to pull funds from this wallet.
print("Awaiting lending approval")
approve_transaction = client.writer.approve_address(
    address=strategy_reserve, 
    amount=LEND_AMOUNT * 10, 
    erc20=erc20
)
client.writer.wait_for_transaction(approve_transaction)
print("Lending approved")

# Lend to a strategy reserve.
print("Begin a deposit")
deposit_transaction = client.writer.deposit(
    LEND_AMOUNT,
    strategy_reserve,
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
print("Lender balance: ", client.reader.get_balance_of(erc20, ETHEREUM_ADDRESS))
