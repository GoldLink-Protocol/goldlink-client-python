"""Constants used in the GoldLink Client for the GMX Funding-rate Farming strategy."""

from goldlink.constants import NETWORK_ID_FUJI

# ------------ Contracts ------------

MANAGER = 'Manager'
ACCOUNT_GETTERS = 'Account Getters'
DATA_STORE = 'Data Store'
GMX_V2_READER = 'GMX V2 Reader'

# ------------ Transactions ------------

CONTRACTS = {
    MANAGER: {
        NETWORK_ID_FUJI: '0xD09b5Daad786a346Ec06a29373473b59965F2146'
    },
    ACCOUNT_GETTERS: {
        NETWORK_ID_FUJI: '0x708dd03D619a7d00cBfC14403733C759cA541951'
    },
    DATA_STORE: {
        NETWORK_ID_FUJI: '0xEA1BFb4Ea9A412dCCd63454AbC127431eBB0F0d4'
    },
    GMX_V2_READER: {
        NETWORK_ID_FUJI: '0x5699dde37406bcA54598813Ee6517758d656daE5'
    }
}
