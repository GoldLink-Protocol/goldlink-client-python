'''Example for lending. Assumes anvil is running.

Usage: python -m examples.lending
'''

from goldlink import Client
from goldlink.constants import NETWORK_ID_ANVIL
from web3 import Web3

# Anvil account + URL.
ETHEREUM_ADDRESS = '0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266'
ETHEREUM_PRIVATE_KEY = '0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80'
WEB_PROVIDER_URL = 'http://127.0.0.1:8545'
ADDRESS_MANAGER_LOCAL = '0x959922bE3CAee4b8Cd9a407cc3ac1C251C2007B1'

client = Client(
    network_id=NETWORK_ID_ANVIL,
    web3=Web3(Web3.HTTPProvider(WEB_PROVIDER_URL)),
)

print(client.reader.get_treasury())
