"""Constants used in the GoldLink Client."""

# ------------ Arbitrum Network IDs ------------
NETWORK_ID_MAINNET = 42161
NETWORK_ID_SEPOLIA = 421614
NETWORK_ID_ANVIL = 31337

# ------------ Signature Types ------------
SIGNATURE_TYPE_NO_PREPEND = 0
SIGNATURE_TYPE_DECIMAL = 1
SIGNATURE_TYPE_HEXADECIMAL = 2

# ------------ Assets ------------
ASSET_USDC = 'USDC'

# ------------ Transactions ------------
DEFAULT_GAS_AMOUNT = 2500000
DEFAULT_GAS_MULTIPLIER = 1.5
DEFAULT_GAS_PRICE = 4000000000
DEFAULT_GAS_PRICE_ADDITION = 3
MAX_SOLIDITY_UINT = 115792089237316195423570985008687907853269984665640564039457584007913129639935  # noqa: E501

CONTRACTS = {
    ASSET_USDC: {
        NETWORK_ID_MAINNET: '0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8',
        NETWORK_ID_SEPOLIA: '0x773330693cb7d5D233348E25809770A32483A940',
        NETWORK_ID_ANVIL: '0x9A9f2CCfdE556A7E9Ff0848998Aa4a0CFD8863AE'
    }
}
COLLATERAL_TOKEN_DECIMALS = 6
DEFAULT_GAS_PRICE_ADDITION = 3

# ------------ API Defaults ------------
DEFAULT_API_TIMEOUT = 3000

# ------------ GoldLink Protocol ABI Paths ------------
ERC20 = 'abi/erc20.json'
GMX_FRF_STRATEGY_ACCOUNT_ABI = 'abi/gmx-frf-strategy-account.json'
STRATEGY_ACCOUNT_ABI = 'abi/strategy-account.json'
STRATEGY_BANK_ABI = 'abi/strategy-bank.json'
STRATEGY_RESERVE_ABI = 'abi/strategy-reserve.json'
