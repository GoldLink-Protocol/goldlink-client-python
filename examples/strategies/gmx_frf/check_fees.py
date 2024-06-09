'''
Example for checking fees.

Usage: python -m examples.strategies.gmx_frf.check_fees
'''

import os
from web3 import Web3
from dotenv import load_dotenv

from goldlink import Client
from goldlink import constants

load_dotenv()

# Load in ENVVAR
STRATEGY_ACCOUNT = os.getenv('GMX_FRF_ACCOUNT')

# Market
WETH_USDC = "0x70d95587d40A2caf56bd97485aB3Eec10Bee6336"

# Tokens
WETH = '0x82aF49447D8a07e3bd95BD0d56f35241523fBab1'
USDC = '0xaf88d065e77c8cC2239327C5EDb3A432268e5831'

# Initialize client.
client = Client(
    network_id=constants.NETWORK_ID_MAINNET,
    web3=Web3(Web3.HTTPProvider(constants.WEB_PROVIDER_URL_ARBITRUM_MAINNET)),
)

print("Get settled funding fees: ", client.gmx_frf_reader.get_settled_funding_fees(STRATEGY_ACCOUNT, WETH_USDC, USDC, WETH))
print("Get settled WETH funding fees: ", client.gmx_frf_reader.get_settled_funding_fees_for_token(STRATEGY_ACCOUNT, WETH_USDC, WETH))
print("Get settled USDC funding fees: ", client.gmx_frf_reader.get_settled_funding_fees_for_token(STRATEGY_ACCOUNT, WETH_USDC, USDC))

claimable_fees = client.gmx_frf_reader.get_position_info(WETH_USDC, STRATEGY_ACCOUNT)['fees']['funding']
print("Get accrued WETH funding fees: ", claimable_fees['claimable_long_token_amount'])
print("Get accrued USDC funding fees: ", claimable_fees['claimable_short_token_amount'])
