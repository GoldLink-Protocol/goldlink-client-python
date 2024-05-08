"""Constants used in the GoldLink Client."""

# ------------  Network IDs ------------
NETWORK_ID_MAINNET = 42161
NETWORK_ID_FUJI = 43113

# ------------  Provider URLs ------------

WEB_PROVIDER_URL_FUJI = 'https://rpc.ankr.com/avalanche_fuji'

# ------------ Signature Types ------------
SIGNATURE_TYPE_NO_PREPEND = 0
SIGNATURE_TYPE_DECIMAL = 1
SIGNATURE_TYPE_HEXADECIMAL = 2

# ------------ Assets ------------
ASSET_USDC = 'USDC'

# ------------ Core Contracts ------------
CONTROLLER = 'Controller'
BANK = 'Bank'
RESERVE = 'Reserve'

# ------------ Transactions ------------
DEFAULT_GAS_AMOUNT = 2500000
DEFAULT_GAS_MULTIPLIER = 1.5
DEFAULT_GAS_PRICE = 4000000000
DEFAULT_GAS_PRICE_ADDITION = 3
MAX_SOLIDITY_UINT = 115792089237316195423570985008687907853269984665640564039457584007913129639935  # noqa: E501

CONTRACTS = {
    ASSET_USDC: {
        NETWORK_ID_MAINNET: '0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8',
        NETWORK_ID_FUJI: '0x3eBDeaA0DB3FfDe96E7a0DBBAFEC961FC50F725F'
    },
    CONTROLLER: {
        NETWORK_ID_FUJI: '0x62be6F58cD141542d3e0d1CB1814e2464cbf3462'
    },
    BANK: {
        NETWORK_ID_FUJI: '0xfc8D0b15999b040A2cF1C6fD4ABF18e6f70E84C7'
    },
    RESERVE: {
        NETWORK_ID_FUJI: '0x4b927EC02cFAB1237eA9e13d5568850Dc0FDFBF5'
    }
}
COLLATERAL_TOKEN_DECIMALS = 6
DEFAULT_GAS_PRICE_ADDITION = 3

# ------------ API Defaults ------------
DEFAULT_API_TIMEOUT = 3000

# ------------ GoldLink Protocol ABI Paths ------------
ERC20 = 'abi/erc20.json'
STRATEGY_ACCOUNT_ABI = 'abi/strategy-account.json'
STRATEGY_BANK_ABI = 'abi/strategy-bank.json'
STRATEGY_RESERVE_ABI = 'abi/strategy-reserve.json'

# ------------ GoldLink Protocol GMX FRF ABI Paths ------------

GMX_FRF_STRATEGY_ACCOUNT_ABI = 'abi/gmx-frf-strategy-account.json'
GMX_FRF_STRATEGY_MANAGER_ABI = 'abi/gmx-frf-strategy-manager.json'
GMX_FRF_ACCOUNT_GETTERS_ABI = 'abi/gmx-frf-account-getters.json'
GMX_V2_READER_ABI = 'abi/gmx_v2_reader.json'
