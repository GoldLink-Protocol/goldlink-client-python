'''
Example for borrowing. Assumes anvil is running. Additionally, only works if
a lending position had been created. Use `python -m examples.lending` to create a 
lending position.

Usage: python -m examples.borrowing
'''

from web3 import Web3
from goldlink import Client
from goldlink.constants import NETWORK_ID_ANVIL
from examples.constants import WEB_PROVIDER_URL, ETHEREUM_ADDRESS, ETHEREUM_PRIVATE_KEY

# Amount to borrow.
BORROW_AMOUNT = 500

# Initialize client.
client = Client(
    network_id=NETWORK_ID_ANVIL,
    web3=Web3(Web3.HTTPProvider(WEB_PROVIDER_URL)),
    private_key=ETHEREUM_PRIVATE_KEY,
    default_address=ETHEREUM_ADDRESS,
)

# Get relevant contract addresses.
omnipool = client.reader.get_omnipool()
prime_brokers = client.reader.get_prime_brokers()
prime_broker_manager = client.reader.get_prime_broker_manager()

# Set approval for PrimeBrokerManager to pull funds from this wallet.
print("Awaiting borrow approval")
approve_transaction = client.writer.approve_address(prime_broker_manager, BORROW_AMOUNT * 10)
client.writer.wait_for_transaction(approve_transaction)
print("Borrow approved")

# Create borrow balance.
print("Opening borrow balance")
balance_transaction = client.writer.execute_borrow(
    prime_brokers[0],
    BORROW_AMOUNT,
    BORROW_AMOUNT,
)
receipt = client.writer.wait_for_transaction(balance_transaction)
borrowEvent = client.event_handler.handle_borrow(receipt)
print("Borrow Event: ", borrowEvent)

# Print effects of borrowing.
print("OmniPool balance: ", client.writer.erc20.functions.balanceOf(omnipool).call())
print("Prime Broker balance: ", client.writer.erc20.functions.balanceOf(prime_brokers[0]).call())
print("Borrower balance: ", client.reader.get_borrower_holdings(prime_brokers[0], ETHEREUM_ADDRESS))
