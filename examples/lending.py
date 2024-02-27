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
erc20_address = client.reader.get_strategy_asset(strategy_reserve=strategy_reserve)
erc20 = client.reader.get_erc20(erc20=erc20_address)

# Get some relevant "before" data points.
before_reserve_balance = erc20.functions.balanceOf(strategy_reserve).call()
print(ETHEREUM_ADDRESS)
print("BEFORE: ", erc20.functions.balanceOf(ETHEREUM_ADDRESS).call())

# Set approval for OmniPool to pull funds from this wallet.
print("Awaiting lending approval")
approve_transaction = client.writer.approve_address(
    address=strategy_reserve, 
    amount=LEND_AMOUNT * 10, 
    erc20=erc20_address
)
client.writer.wait_for_transaction(approve_transaction)
print("Lending approved")

# Lend to a single strategy.
print("Opening lending position")
position_transaction = client.writer.deposit(
    LEND_AMOUNT,
    strategy_reserve,
)
receipt = client.writer.wait_for_transaction(position_transaction)
depositEvent = client.event_handler.handle_deposit_event(
    strategy_reserve,
    receipt
)
print("Open Position Event: ", depositEvent)

# Verify lending succeeded.
after_reserve_balance = erc20.functions.balanceOf(strategy_reserve).call()

assert after_reserve_balance - before_reserve_balance == LEND_AMOUNT
print("Lending position verified")

# Print effects of lending.
print("Strategy Reserve balance: ", erc20.functions.balanceOf(strategy_reserve).call())
print("Lender balance: ", erc20.functions.balanceOf(ETHEREUM_ADDRESS).call())
