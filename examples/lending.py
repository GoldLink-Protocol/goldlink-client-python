'''Example for lending. Assumes anvil is running.

Usage: python -m examples.lending
'''

from web3 import Web3
from goldlink import Client
from goldlink.constants import NETWORK_ID_ANVIL
from examples.constants import WEB_PROVIDER_URL, ETHEREUM_ADDRESS, ETHEREUM_PRIVATE_KEY

# Amount to lend.
LEND_AMOUNT = 10000

# Initialize client.
client = Client(
    network_id=NETWORK_ID_ANVIL,
    web3=Web3(Web3.HTTPProvider(WEB_PROVIDER_URL)),
    private_key=ETHEREUM_PRIVATE_KEY,
    default_address=ETHEREUM_ADDRESS,
)

# Get relevant contract addresses.
strategies = client.reader.get_strategy_pools()
omnipool = client.reader.get_omnipool()

# Get some relevant "before" data points.
before_omnipool_balance = client.writer.erc20.functions.balanceOf(omnipool).call()
before_enrolled_funds = client.reader.get_total_enrolled_funds(strategies[0])

# Set approval for OmniPool to pull funds from this wallet
print("Awaiting lending approval")
approve_transaction = client.writer.approve_address(omnipool, LEND_AMOUNT * 10)
client.writer.wait_for_transaction(approve_transaction)
print("Lending approved")

# Lend to a single strategy.
print("Opening lending position")
position_transaction = client.writer.execute_open_position(
    LEND_AMOUNT,
    [strategies[0]],
    [1 * 10 ** 18],
    ETHEREUM_ADDRESS,
)
client.writer.wait_for_transaction(position_transaction)

# Verify lending succeeded.
position = client.reader.get_position(1)
after_omnipool_balance = client.writer.erc20.functions.balanceOf(omnipool).call()
after_enrolled_funds = client.reader.get_total_enrolled_funds(strategies[0])

assert after_omnipool_balance - before_omnipool_balance == LEND_AMOUNT
assert after_enrolled_funds - before_enrolled_funds == LEND_AMOUNT
assert position[0] == LEND_AMOUNT
assert position[2] == [1 * 10 ** 18]
print("Lending position verified")

# Print effects of lending.
print("OmniPool balance: ", client.writer.erc20.functions.balanceOf(omnipool).call())
print("Position: ", client.reader.get_position(1))
print("Strategy1 enrollment: ", client.reader.get_total_enrolled_funds(strategies[0]))
