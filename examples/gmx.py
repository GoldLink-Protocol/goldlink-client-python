'''
Example for calling all execute calls for the GMX FRF Strategy. Note: the deployed strategy on Arbitrum Sepolia is
a pass-through that emits events and otherwise does nothing.

Usage: python -m examples.gmx
'''

import os
from web3 import Web3
from dotenv import load_dotenv

from goldlink import Client
from goldlink.constants import NETWORK_ID_SEPOLIA

from examples.constants import WEB_PROVIDER_URL

## Sepolia Contracts
## Controller: https://sepolia.arbiscan.io/address/0x4BB8CEC268d5b37C441447bBd1368Aa435b9bc3f
## Mock ERC20: https://sepolia.arbiscan.io/address/0x614B2EA1Ba52a974c4d270B6E13C8b0Abb8e4cB0
## Bank: https://sepolia.arbiscan.io/address/0x9f74A47Cea41dD898F945EF6B729E64176805b26
## Reserve: https://sepolia.arbiscan.io/address/0x27E0d1C15b184972D09878f6fF868c2163f19DCC

load_dotenv()

# Load in ENVVAR
PUBLIC_KEY = os.getenv('TEST_OWNER_PUBLIC_KEY')
PRIVATE_KEY = os.getenv('TEST_OWNER_PRIVATE_KEY')
GMX_FRF_ACCOUNT = os.getenv('GMX_FRF_ACCOUNT')

# Initialize client.
client = Client(
    network_id=NETWORK_ID_SEPOLIA,
    web3=Web3(Web3.HTTPProvider(WEB_PROVIDER_URL)),
    private_key=PRIVATE_KEY,
    default_address=PUBLIC_KEY,
)

# Get relevant contract addresses.
strategy_bank = "0x9f74A47Cea41dD898F945EF6B729E64176805b26"
erc20 = client.reader.get_strategy_asset(strategy_bank=strategy_bank)

strategy_account = GMX_FRF_ACCOUNT

options = {
    'gasPrice': 1000000000
}

create_increase_transaction = client.gmx_frf_writer.create_increase_order(
    strategy_account=strategy_account,
    market="0x614B2EA1Ba52a974c4d270B6E13C8b0Abb8e4cB0", 
    amount=100,
    send_options=options
)
receipt = client.gmx_frf_writer.wait_for_transaction(create_increase_transaction)
create_increase_order_event = client.gmx_frf_event_handler.handle_create_increase_order_event(strategy_account, receipt)
print("Increase order: ", create_increase_order_event.order)

create_decrease_transaction = client.gmx_frf_writer.create_decrease_order(
    strategy_account=strategy_account,
    market="0x614B2EA1Ba52a974c4d270B6E13C8b0Abb8e4cB0", 
    size_delta_usd=100,
    send_options=options
)
receipt = client.gmx_frf_writer.wait_for_transaction(create_decrease_transaction)
create_decrease_order_event = client.gmx_frf_event_handler.handle_create_decrease_order_event(strategy_account, receipt)
print("Decrease order: ", create_decrease_order_event.order)

claim_collateral_transaction = client.gmx_frf_writer.claim_collateral(
    strategy_account=strategy_account,
    market="0x614B2EA1Ba52a974c4d270B6E13C8b0Abb8e4cB0",
    asset= "0x614B2EA1Ba52a974c4d270B6E13C8b0Abb8e4cB0",
    time_key=50,
    send_options=options
)
receipt = client.gmx_frf_writer.wait_for_transaction(claim_collateral_transaction)
claim_collateral_event = client.gmx_frf_event_handler.handle_claim_collateral_event(strategy_account, receipt)
print("Claim collateral: ", claim_collateral_event)

claim_funding_fees_transaction = client.gmx_frf_writer.claim_funding_fees(
    strategy_account=strategy_account,
    markets=["0x614B2EA1Ba52a974c4d270B6E13C8b0Abb8e4cB0", "0x773330693cb7d5D233348E25809770A32483A940"],
    assets=["0x614B2EA1Ba52a974c4d270B6E13C8b0Abb8e4cB0", "0x773330693cb7d5D233348E25809770A32483A940"],
    send_options=options
)
receipt = client.gmx_frf_writer.wait_for_transaction(claim_funding_fees_transaction)
claim_funding_fees_event = client.gmx_frf_event_handler.handle_claim_funding_fees_event(strategy_account, receipt)
print("Claim funding fees: ", claim_funding_fees_event)

cancel_order_transaction = client.gmx_frf_writer.cancel_order(
    strategy_account=strategy_account,
    order_key=bytes('0x010', 'utf-8'),
    send_options=options
)
receipt = client.gmx_frf_writer.wait_for_transaction(cancel_order_transaction)
cancel_order_event = client.gmx_frf_event_handler.handle_cancel_order_event(strategy_account, receipt)
print("Cancel order: ", cancel_order_event)

liquidate_assets_transaction = client.gmx_frf_writer.liquidate_assets(
    strategy_account=strategy_account,
    asset="0x614B2EA1Ba52a974c4d270B6E13C8b0Abb8e4cB0",
    amount=120,
    callback="0x614B2EA1Ba52a974c4d270B6E13C8b0Abb8e4cB0",
    receiver=PUBLIC_KEY,
    send_options=options
)
receipt = client.gmx_frf_writer.wait_for_transaction(liquidate_assets_transaction)
liquidate_assets_event = client.gmx_frf_event_handler.handle_liquidate_assets_event(strategy_account, receipt)
print("Liquidate assets: ", liquidate_assets_event)


liquidate_position_transaction = client.gmx_frf_writer.liquidate_position(
    strategy_account=strategy_account,
    market="0x614B2EA1Ba52a974c4d270B6E13C8b0Abb8e4cB0",
    size_delta_usd=120,
    send_options=options
)
receipt = client.gmx_frf_writer.wait_for_transaction(liquidate_position_transaction)
liquidate_position_event = client.gmx_frf_event_handler.handle_liquidate_position_event(strategy_account, receipt)
print("Liquidate position: ", liquidate_position_event)

rebalance_position_transaction = client.gmx_frf_writer.rebalance_position(
    strategy_account=strategy_account,
    market="0x614B2EA1Ba52a974c4d270B6E13C8b0Abb8e4cB0",
    send_options=options
)
receipt = client.gmx_frf_writer.wait_for_transaction(rebalance_position_transaction)
rebalance_position_event = client.gmx_frf_event_handler.handle_rebalance_position_event(strategy_account, receipt)
print("Rebalance position: ", rebalance_position_event)

releverage_position_transaction = client.gmx_frf_writer.releverage_position(
    strategy_account=strategy_account,
    market="0x614B2EA1Ba52a974c4d270B6E13C8b0Abb8e4cB0",
    size_delta_usd=10000,
    send_options=options
)
receipt = client.gmx_frf_writer.wait_for_transaction(releverage_position_transaction)
releverage_position_event = client.gmx_frf_event_handler.handle_releverage_position_event(strategy_account, receipt)
print("Releverage position: ", releverage_position_event)

swap_rebalance_transaction = client.gmx_frf_writer.swap_rebalance(
    strategy_account=strategy_account,
    market="0x614B2EA1Ba52a974c4d270B6E13C8b0Abb8e4cB0",
    callback_config=(
        "0x614B2EA1Ba52a974c4d270B6E13C8b0Abb8e4cB0",
        PUBLIC_KEY,
        1000,
    ),
    send_options=options
)
receipt = client.gmx_frf_writer.wait_for_transaction(swap_rebalance_transaction)
swap_rebalance_event = client.gmx_frf_event_handler.handle_swap_rebalance_event(strategy_account, receipt)
print("Swap rebalance: ", swap_rebalance_event)
