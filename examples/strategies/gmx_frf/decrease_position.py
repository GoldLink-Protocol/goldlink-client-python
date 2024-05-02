'''
Example for decreasing a position. Additionally, only works if
a GMX position had been created. Use `python -m examples.strategies.gmx_frf.increase_position` to create a
GMX position on Fuji.

Usage: python -m examples.strategies.gmx_frf.decrease_position
'''

import os
from web3 import Web3
from dotenv import load_dotenv

from goldlink import Client
from goldlink import constants

load_dotenv()

# Load in ENVVAR
PUBLIC_KEY = os.getenv('TEST_OWNER_PUBLIC_KEY')
PRIVATE_KEY = os.getenv('TEST_OWNER_PRIVATE_KEY')
STRATEGY_ACCOUNT = os.getenv('GMX_FRF_ACCOUNT')

# Market
GMX_MARKET = "0xD996ff47A1F763E1e55415BC4437c59292D1F415"

# Initialize client.
client = Client(
    network_id=constants.NETWORK_ID_FUJI,
    web3=Web3(Web3.HTTPProvider(constants.WEB_PROVIDER_URL_FUJI)),
    private_key=PRIVATE_KEY,
    strategy_account=STRATEGY_ACCOUNT,
)

options = {
    'gasPrice': 25000000000,
    'value': 2500000000000000000
}

print(client.reader.get_account_value(strategy_account=STRATEGY_ACCOUNT))

# Decrease position.
print("Decreasing GMX Market position")
decrease_position_transaction = client.gmx_frf_writer.create_decrease_order(
    market=GMX_MARKET,
    size_delta_usd=60000000,
    execution_fee=2500000000000000000,
    send_options=options
)
receipt = client.gmx_frf_writer.wait_for_transaction(decrease_position_transaction)
print("Create decrease order event: ", client.gmx_frf_event_handler.handle_create_decrease_order_event(STRATEGY_ACCOUNT, receipt))
