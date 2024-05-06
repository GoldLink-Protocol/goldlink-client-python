'''
Example for getting complex information. Additionally, some queries only work if
a GMX position had been created. Use `python -m examples.strategies.gmx_frf.increase_position` to create a
GMX position on Fuji.

Usage: python -m examples.strategies.gmx_frf.get_info
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
)

client.strategy_account = STRATEGY_ACCOUNT

print("Referral storage:", client.gmx_frf_reader.get_referral_storage())
print("Market token Addresses: ", client.gmx_frf_reader.get_token_addresses_for_market(GMX_MARKET))
print("Position: ", client.gmx_frf_reader.get_position(GMX_MARKET, STRATEGY_ACCOUNT))
print("Market Info: ", client.gmx_frf_reader.get_market_info(GMX_MARKET))
print("Position info: ", client.gmx_frf_reader.get_position_info(GMX_MARKET, STRATEGY_ACCOUNT))
