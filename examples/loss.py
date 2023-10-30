'''
Simulate loss in a strategy. Assumes a borrower holding has been created.

Usage: python -m examples.loss
'''

from web3 import Web3
from goldlink import Client
from goldlink.constants import NETWORK_ID_ANVIL
from examples.constants import WEB_PROVIDER_URL, ETHEREUM_ADDRESS, ETHEREUM_PRIVATE_KEY

# Amount to lose.
LOSS_AMOUNT = 250

# Initialize client.
client = Client(
    network_id=NETWORK_ID_ANVIL,
    web3=Web3(Web3.HTTPProvider(WEB_PROVIDER_URL)),
    private_key=ETHEREUM_PRIVATE_KEY,
    default_address=ETHEREUM_ADDRESS,
)

# Get relevant contract addresses.
prime_brokers = client.reader.get_prime_brokers()
prime_broker_manager = client.reader.get_prime_broker_manager()

old_holdings =  client.reader.get_borrower_holdings(prime_brokers[0], ETHEREUM_ADDRESS);
old_health_score = client.reader.get_health_score(prime_brokers[0], old_holdings)
print("Old health score: ", old_health_score)

# Record loss in the prime broker.
print("Experience loss")
balance_transaction = client.writer.update_for_strategy_performance(
    prime_brokers[0],
    LOSS_AMOUNT,
    False,
)
client.writer.wait_for_transaction(balance_transaction)

holdings =  client.reader.get_borrower_holdings(prime_brokers[0], ETHEREUM_ADDRESS);
health_score = client.reader.get_health_score(prime_brokers[0], holdings)

# Print effects of loss.
print("Health score: ", health_score)
print("Share price: ", client.reader.get_prime_broker_share_price(prime_brokers[0]))
