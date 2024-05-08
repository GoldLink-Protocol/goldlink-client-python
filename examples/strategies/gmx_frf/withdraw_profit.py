'''
Example for withdrawing profit. Additionally, only works if account has profit to withdraw, the market is
not overly short and the profit respects the buffer.

Usage: python -m examples.strategies.gmx_frf.withdraw_profit
'''

import os
from web3 import Web3
from dotenv import load_dotenv

from goldlink import Client
from goldlink import constants
from goldlink.modules.strategies.gmx_frf.constants import MANAGER, ACCOUNT_GETTERS, CONTRACTS

load_dotenv()

# Load in ENVVAR
PUBLIC_KEY = os.getenv('TEST_OWNER_PUBLIC_KEY')
PRIVATE_KEY = os.getenv('TEST_OWNER_PRIVATE_KEY')
STRATEGY_ACCOUNT = os.getenv('GMX_FRF_ACCOUNT')

# Market
AVAX_USDC = "0xD996ff47A1F763E1e55415BC4437c59292D1F415"

# Initialize client.
client = Client(
    network_id=constants.NETWORK_ID_FUJI,
    web3=Web3(Web3.HTTPProvider(constants.WEB_PROVIDER_URL_FUJI)),
    private_key=PRIVATE_KEY,
    strategy_account=STRATEGY_ACCOUNT,
)

options = {
    'gasPrice': 25000000000
}

manager = CONTRACTS[MANAGER][constants.NETWORK_ID_FUJI]
account_getters = CONTRACTS[ACCOUNT_GETTERS][constants.NETWORK_ID_FUJI]

# Get current position value.
print(client.gmx_frf_reader.get_position_value_usd(
    strategy_account=STRATEGY_ACCOUNT,
    market=AVAX_USDC
))

# Withdraw profit.
print("Withdrawing profit")
withdraw_profit_transaction = client.gmx_frf_writer.withdraw_profit(
    params={
        'market': AVAX_USDC,
        'amount': 10000,
        'recipient': PUBLIC_KEY
    },
    send_options=options
)
receipt = client.gmx_frf_writer.wait_for_transaction(withdraw_profit_transaction)
print("Withdraw profit event: ", client.gmx_frf_event_handler.handle_withdraw_profit_event(STRATEGY_ACCOUNT, receipt))
