"""Constants used in the GoldLink Client for the GMX Funding-rate Farming strategy."""

from goldlink import constants

# ------------ Contracts ------------

MANAGER = 'Manager'
ACCOUNT_GETTERS = 'Account Getters'

# ------------ Transactions ------------

CONTRACTS = {
    MANAGER: {
        constants.NETWORK_ID_FUJI: '0xA856cA6057Db7d97D5c25b5798e417cf97E32931'
    },
    ACCOUNT_GETTERS: {
        constants.NETWORK_ID_FUJI: '0xc2A154ec32445b8f254B49ddA6459027010c06a9'
    }
}
