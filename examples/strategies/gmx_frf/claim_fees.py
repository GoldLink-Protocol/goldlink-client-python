'''
Example for claiming fees. Additionally, only works if
a GMX position had been created. Use `python -m examples.strategies.gmx_frf.increase_position` to create a 
GMX position on Fuji.

Usage: python -m examples.strategies.gmx_frf.claim_fees
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
GMX_MARKET="0xD996ff47A1F763E1e55415BC4437c59292D1F415"

# Initialize client.
client = Client(
    network_id=constants.NETWORK_ID_FUJI,
    web3=Web3(Web3.HTTPProvider(constants.WEB_PROVIDER_URL_FUJI)),
    private_key=PRIVATE_KEY,
)

client.strategy_account = STRATEGY_ACCOUNT

options = {
    'gasPrice': 25000000000
}

USDC = constants.CONTRACTS[constants.ASSET_USDC][constants.NETWORK_ID_FUJI]

# Increase position.
print("Claiming fees for one or more GMX Market position")
claim_fees_transaction = client.gmx_frf_writer.claim_funding_fees(
    markets=[GMX_MARKET],
    assets=[USDC],
    send_options=options
)
receipt = client.gmx_frf_writer.wait_for_transaction(claim_fees_transaction)
print("Claim Fees event: ", client.gmx_frf_event_handler.handle_claim_funding_fees_event(STRATEGY_ACCOUNT, receipt))

