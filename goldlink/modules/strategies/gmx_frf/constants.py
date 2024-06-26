"""Constants used in the GoldLink Client for the GMX Funding-rate Farming strategy."""

from goldlink.constants import NETWORK_ID_FUJI, NETWORK_ID_MAINNET

# ------------ Contracts ------------

MANAGER = 'Manager'
ACCOUNT_GETTERS = 'Account Getters'
DATA_STORE = 'Data Store'
GMX_V2_READER = 'GMX V2 Reader'

# ------------ Transactions ------------

CONTRACTS = {
    MANAGER: {
        NETWORK_ID_MAINNET: '0x975B4a621D937605Eaeb117C00653CfBFbFb46CC',
        NETWORK_ID_FUJI: '0xD09b5Daad786a346Ec06a29373473b59965F2146'
    },
    ACCOUNT_GETTERS: {
        NETWORK_ID_MAINNET: '0xe6e6E3a44b5c881D02f4BD89Df84BBF18DeE2E5D',
        NETWORK_ID_FUJI: '0x708dd03D619a7d00cBfC14403733C759cA541951'
    },
    DATA_STORE: {
        NETWORK_ID_MAINNET: '0xFD70de6b91282D8017aA4E741e9Ae325CAb992d8',
        NETWORK_ID_FUJI: '0xEA1BFb4Ea9A412dCCd63454AbC127431eBB0F0d4'
    },
    GMX_V2_READER: {
        NETWORK_ID_MAINNET: '0x60a0fF4cDaF0f6D496d71e0bC0fFa86FE8E6B23c',
        NETWORK_ID_FUJI: '0x5699dde37406bcA54598813Ee6517758d656daE5'
    }
}
