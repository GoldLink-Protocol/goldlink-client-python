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
        NETWORK_ID_FUJI: '0xA856cA6057Db7d97D5c25b5798e417cf97E32931'
    },
    ACCOUNT_GETTERS: {
        NETWORK_ID_FUJI: '0xc2A154ec32445b8f254B49ddA6459027010c06a9'
    },
    DATA_STORE: {
        NETWORK_ID_FUJI: '0xEA1BFb4Ea9A412dCCd63454AbC127431eBB0F0d4'
    },
    GMX_V2_READER: {
        NETWORK_ID_FUJI: '0x5699dde37406bcA54598813Ee6517758d656daE5'
    }
}
