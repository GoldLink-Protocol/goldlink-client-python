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

# Set approval for OmniPool to pull funds from this wallet
print("Awaiting approval")
transaction2 = client.writer.approve_address(omnipool, LEND_AMOUNT * 10)
client.writer.wait_for_transaction(transaction2)
print("Approved")

# Lend to a single strategy.
transaction = client.writer.execute_open_position(
    LEND_AMOUNT,
    [strategies[0]], [1 * 10 ** 18],
    ETHEREUM_ADDRESS,
)
client.writer.wait_for_transaction(transaction)

# Verify lending succeeded.
print(client.writer.erc20.functions.balanceOf(omnipool).call())
print(client.reader.get_position(1))
print(client.reader.get_total_enrolled_funds(strategies[0]))
