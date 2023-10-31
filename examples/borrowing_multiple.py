'''
Example for borrowing across multiple accounts. Assumes anvil is running. Additionally, only works if
a lending position had been created. Use `python -m examples.lending` to create a 
lending position.

Usage: python -m examples.borrowing_multiple
'''

from web3 import Web3
from goldlink import Client
from goldlink.constants import NETWORK_ID_ANVIL
from examples.constants import WEB_PROVIDER_URL, ETHEREUM_ADDRESS, ETHEREUM_PRIVATE_KEY, ETHEREUM_ADDRESS_2, ETHEREUM_PRIVATE_KEY_2

# Amount to borrow.
BORROW_AMOUNT = 500

# Initialize clients.
client = Client(
    network_id=NETWORK_ID_ANVIL,
    web3=Web3(Web3.HTTPProvider(WEB_PROVIDER_URL)),
    private_key=ETHEREUM_PRIVATE_KEY,
    default_address=ETHEREUM_ADDRESS,
)
client_2 = Client(
    network_id=NETWORK_ID_ANVIL,
    web3=Web3(Web3.HTTPProvider(WEB_PROVIDER_URL)),
    private_key=ETHEREUM_PRIVATE_KEY_2,
    default_address=ETHEREUM_ADDRESS_2,
)

# Get relevant contract addresses.
omnipool = client.reader.get_omnipool()
prime_brokers = client.reader.get_prime_brokers()
prime_broker_manager = client.reader.get_prime_broker_manager()

# Set approval for PrimeBrokerManager to pull funds from this wallet.
print("Awaiting borrow approval")
approve_transaction = client.writer.approve_address(prime_broker_manager, BORROW_AMOUNT * 10)
client.writer.wait_for_transaction(approve_transaction)
approve_transaction = client_2.writer.approve_address(prime_broker_manager, BORROW_AMOUNT * 10)
client_2.writer.wait_for_transaction(approve_transaction)
print("Borrow approved")

# Transfer assets to client 2.
transfer_transaction = client.writer.transfer(ETHEREUM_ADDRESS_2, BORROW_AMOUNT)
client.writer.wait_for_transaction(transfer_transaction)

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

# Create borrow balance for client 2.
print("Opening borrow balance")
balance_transaction = client_2.writer.execute_borrow(
    prime_brokers[0],
    BORROW_AMOUNT,
    BORROW_AMOUNT,
)
receipt = client_2.writer.wait_for_transaction(balance_transaction)
borrowEvent = client_2.event_handler.handle_borrow(receipt)
print("Borrow Event: ", borrowEvent)

# Print effects of borrowing.
print("OmniPool balance: ", client.writer.erc20.functions.balanceOf(omnipool).call())
print("Prime Broker balance: ", client.writer.erc20.functions.balanceOf(prime_brokers[0]).call())
print("Borrower balance: ", client.reader.get_borrower_holdings(prime_brokers[0], ETHEREUM_ADDRESS))
print("Borrower 2 balance: ", client.reader.get_borrower_holdings(prime_brokers[0], ETHEREUM_ADDRESS_2))

