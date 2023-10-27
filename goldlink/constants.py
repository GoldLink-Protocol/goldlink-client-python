"""Constants used in the GoldLink Client."""

# ------------ Arbitrum Network IDs ------------
NETWORK_ID_MAINNET = 42161
NETWORK_ID_GOERLI = 421613
NETWORK_ID_ANVIL = 31337

# ------------ Signature Types ------------
SIGNATURE_TYPE_NO_PREPEND = 0
SIGNATURE_TYPE_DECIMAL = 1
SIGNATURE_TYPE_HEXADECIMAL = 2

# ------------ Assets ------------
ASSET_USDC = 'USDC'
ADDRESS_MANAGER = 'ADDRESS_MANAGER'

# ------------ Transactions ------------
DEFAULT_GAS_AMOUNT = 2500000
DEFAULT_GAS_MULTIPLIER = 1.5
DEFAULT_GAS_PRICE = 4000000000
DEFAULT_GAS_PRICE_ADDITION = 3
MAX_SOLIDITY_UINT = 115792089237316195423570985008687907853269984665640564039457584007913129639935  # noqa: E501

CONTRACTS = {
    ASSET_USDC: {
        NETWORK_ID_MAINNET: '0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8',
        NETWORK_ID_GOERLI: '0xfd064A18f3BF249cf1f87FC203E90D8f650f2d63',
        NETWORK_ID_ANVIL: '0x5FbDB2315678afecb367f032d93F642f64180aa3'
    },
    ADDRESS_MANAGER: {
        NETWORK_ID_ANVIL: '0x9fE46736679d2D9a65F0992F2272dE9f3c7fa6e0'
    }
}
COLLATERAL_TOKEN_DECIMALS = 6
DEFAULT_GAS_PRICE_ADDITION = 3

# ------------ API Defaults ------------
DEFAULT_API_TIMEOUT = 3000

# ------------ GoldLink Protocol ABI Paths ------------
ADDRESS_MANAGER_ABI = 'abi/address-manager.json'
OMNIPOOL_ABI = 'abi/omnipool.json'
PRIME_BROKER_MANAGER_ABI = 'abi/prime-broker-manager.json'
STRATEGY_POOL_ABI = 'abi/strategy-pool.json'
PRIME_BROKER_ABI = 'abi/prime-broker.json'
ERC20 = 'abi/erc20.json'
