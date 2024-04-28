'''
Example for increasing a position. Additionally, only works if
a lending position had been created. Use `python -m examples.lending` to create a 
lending position on Fuji.

Usage: python -m examples.strategies.gmx_frf.increase_position
'''

import os
from web3 import Web3
from dotenv import load_dotenv

from goldlink import Client
from goldlink.modules.strategies.gmx_frf.constants import MANAGER, ACCOUNT_GETTERS, CONTRACTS
from goldlink import constants

load_dotenv()

# Load in ENVVAR
PUBLIC_KEY = os.getenv('TEST_OWNER_PUBLIC_KEY')
PRIVATE_KEY = os.getenv('TEST_OWNER_PRIVATE_KEY')
STRATEGY_ACCOUNT = os.getenv('GMX_FRF_ACCOUNT')

# Market
GMX_MARKET="0xD996ff47A1F763E1e55415BC4437c59292D1F415"

# Initialize client.
client = Client(
    network_id=constants.NETWORK_ID_FUJI,
    web3=Web3(Web3.HTTPProvider(constants.WEB_PROVIDER_URL_FUJI)),
    private_key=PRIVATE_KEY,
    default_address=PUBLIC_KEY,
)

options = {
    'gasPrice': 25000000000,
    'value': 2500000000000000000
}

# Increase position.
print("Increasing GMX Market position")
increase_position_transaction = client.gmx_frf_writer.create_increase_order(
    strategy_account=STRATEGY_ACCOUNT,
    market=GMX_MARKET,
    amount=60000000,
    execution_fee=2500000000000000000,
    send_options=options
)
receipt = client.gmx_frf_writer.wait_for_transaction(increase_position_transaction)
print("Create increase order event: ", client.gmx_frf_event_handler.handle_create_increase_order_event(STRATEGY_ACCOUNT, receipt))


