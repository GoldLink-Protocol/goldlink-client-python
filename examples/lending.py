'''Example for lending. Assumes anvil is running.

Usage: python -m examples.lending
'''

from web3 import Web3
from goldlink import Client
from goldlink.constants import NETWORK_ID_ANVIL

# Anvil URL, address, private key.
WEB_PROVIDER_URL = 'http://127.0.0.1:8545'
ETHEREUM_ADDRESS = '0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266'
ETHEREUM_PRIVATE_KEY = '0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80'

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
transaction = client.writer.execute_new_supply(
    LEND_AMOUNT,
    [strategies[0]], [1 * 10 ** 18],
    ETHEREUM_ADDRESS,
)
client.writer.wait_for_transaction(transaction)

# Verify lending succeeded.
print(client.writer.erc20.functions.balanceOf(omnipool).call())
print(client.reader.get_receipt_information(1))
print(client.reader.get_total_enrolled_funds(strategies[0]))
