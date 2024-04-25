'''
Example for increasing a position. Additionally, only works if account has profit to withdraw.

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
GMX_MARKET="0xD996ff47A1F763E1e55415BC4437c59292D1F415"

# Initialize client.
client = Client(
    network_id=constants.NETWORK_ID_FUJI,
    web3=Web3(Web3.HTTPProvider(constants.WEB_PROVIDER_URL_FUJI)),
    private_key=PRIVATE_KEY,
    default_address=PUBLIC_KEY,
)

options = {
    'gasPrice': 25000000000
}

print(client.reader.get_account_value(strategy_account=STRATEGY_ACCOUNT))

manager = CONTRACTS[MANAGER][constants.NETWORK_ID_FUJI]
account_getters = CONTRACTS[ACCOUNT_GETTERS][constants.NETWORK_ID_FUJI]

# Withdraw profit.
# print("Available markets: ", client.gmx_frf_reader.get_available_markets(strategy_manager=manager))
print("getter: ", client.gmx_frf_reader.get_account_positions_value_usd(account_getters=account_getters, strategy_manager=manager, strategy_account=STRATEGY_ACCOUNT))
# print("Withdrawing profit")
# withdraw_profit_transaction = client.gmx_frf_writer.withdraw_profit(
#     strategy_account=STRATEGY_ACCOUNT,
#     params={
#         'market': GMX_MARKET,
#         'amount': 0,
#         'recipient': PUBLIC_KEY
#     },
#     send_options=options
# )
# receipt = client.gmx_frf_writer.wait_for_transaction(withdraw_profit_transaction)
# print("Withdraw profit event: ", client.gmx_frf_event_handler.handle_withdraw_profit_event(STRATEGY_ACCOUNT, receipt))
