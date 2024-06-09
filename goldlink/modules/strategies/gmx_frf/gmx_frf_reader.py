"""Module providing access to methods for reading from GoldLink Contracts for the GMX Funding-rate Farming strategy."""

from web3 import Web3
from eth_abi import encode_abi

from goldlink.modules.contract_handler import ContractHandler
from goldlink.helpers import send_raw_query
from goldlink.modules.strategies.gmx_frf.constants import CONTRACTS, ACCOUNT_GETTERS, MANAGER, GMX_V2_READER, DATA_STORE


class GmxFrfReader(ContractHandler):
    '''
    Module for reading from the GoldLink Protocol for the GMX Funding-rate Farming strategy.
    '''

    def __init__(
        self,
        web3,
        network_id,
    ):
        ContractHandler.__init__(self, web3)

        self.network_id = network_id

        # Set strategy specific addresses.
        self.account_getters_address = CONTRACTS[ACCOUNT_GETTERS][self.network_id]
        self.gmx_v2_reader_address = CONTRACTS[GMX_V2_READER][self.network_id]
        self.manager_address = CONTRACTS[MANAGER][self.network_id]
        self.data_store_address = CONTRACTS[DATA_STORE][self.network_id]

        # Set strategy specific contracts.
        self.manager = self.get_gmxfrf_strategy_manager(self.manager_address)
        self.gmx_v2_reader = self.get_gmx_v2_reader(self.gmx_v2_reader_address)
        self.igmx_v2_datastore = self.get_igmx_v2_datastore(self.data_store_address)

    # -----------------------------------------------------------
    # Strategy Config Querying Functions
    # -----------------------------------------------------------

    def get_asset_liquidation_fee_percent(self, asset):
        '''
        Get the asset liquidation fee percent for the strategy.

        :param asset: required
        :type asset: address

        :returns: integer
        '''
        return self.manager.functions.liquidationFeePercent(asset).call()

    def get_callback_gas_limit(self):
        '''
        Get the callback gas limit for the strategy.

        :returns: integer
        '''
        return self.manager.functions.getCallbackGasLimit().call()

    def get_execution_fee_buffer_percent(self):
        '''
        Get the execution fee buffer percent for the strategy.

        :returns: integer
        '''
        return self.manager.functions.getExecutionFeeBufferPercent().call()

    def get_liquidation_order_timeout_deadline(self):
        '''
        Get the liquidation order timeout deadline for the strategy.

        :returns: integer
        '''
        return self.manager.functions.getLiquidationOrderTimeoutDeadline().call()

    def get_profit_withdrawal_buffer_percent(self):
        '''
        Get the profit withdrawal buffer percent for the strategy.

        :returns: integer
        '''
        return self.manager.functions.getProfitWithdrawalBufferPercent().call()

    def get_referral_code(self):
        '''
        Get the referral code for the strategy.

        :returns: bytes
        '''
        return self.manager.functions.getReferralCode().call()

    # -----------------------------------------------------------
    # Market Querying Functions
    # -----------------------------------------------------------

    def get_token_addresses_for_market(self, market):
        '''
        Get addresses for market.

        :param market: required
        :type market: address

        :returns: Object
        '''
        token_addresses = self.gmx_v2_reader.functions.getMarket(
            self.data_store_address,
            market
        ).call()

        return {
            "market_token": token_addresses[0],
            "index_token": token_addresses[1],
            "long_token": token_addresses[2],
            "short_token": token_addresses[3],
        }

    def get_market_info(self, market):
        '''
        Get market information.

        :param market: required
        :type market: address

        :returns: Object
        '''
        market_addresses = self.get_token_addresses_for_market(market)
        short_prices = self.get_asset_price(market_addresses['short_token'])
        long_prices = self.get_asset_price(market_addresses['long_token'])

        market_info = self.gmx_v2_reader.functions.getMarketInfo(
            self.data_store_address,
            (
                (long_prices["price"], long_prices["price"]),
                (long_prices["price"], long_prices["price"]),
                (short_prices["price"], short_prices["price"]),
            ),
            market
        ).call()

        return {
            "market": {
                "market_token": market_info[0][0],
                "index_token": market_info[0][1],
                "long_token": market_info[0][2],
                "short_token": market_info[0][3],
            },
            "borrowing_factor_per_second_for_longs": market_info[1],
            "borrowing_factor_per_second_for_shorts": market_info[2],
            "base_funding": {
                "funding_fee_amount_per_size": {
                    "long": {
                        "long_token": market_info[3][0][0][0],
                        "short_token": market_info[3][0][0][1],
                    },
                    "short": {
                        "long_token": market_info[3][0][1][0],
                        "short_token": market_info[3][0][1][1],
                    },
                },
                "claimable_funding_amount_per_size": {
                    "long": {
                        "long_token": market_info[3][1][0][0],
                        "short_token": market_info[3][1][0][1],
                    },
                    "short": {
                        "long_token": market_info[3][1][1][0],
                        "short_token": market_info[3][1][1][1],
                    },
                }
            },
            "next_funding": {
                "longs_pay_shorts": market_info[4][0],
                "funding_factor_per_second": market_info[4][1],
                "next_saved_funding_factor_per_second": market_info[4][2],
                "funding_fee_amount_per_size_delta": {
                    "long": {
                        "long_token": market_info[4][3][0][0],
                        "short_token": market_info[4][3][0][1],
                    },
                    "short": {
                        "long_token": market_info[4][3][1][0],
                        "short_token": market_info[4][3][1][1],
                    },
                },
                "claimable_funding_amount_per_size_delta": {
                    "long": {
                        "long_token": market_info[4][4][0][0],
                        "short_token": market_info[4][4][0][1],
                    },
                    "short": {
                        "long_token": market_info[4][4][1][0],
                        "short_token": market_info[4][4][1][1],
                    },
                },
            },
            "virtual_inventory": {
                "virtual_pool_amount_for_long_token": market_info[5][0],
                "virtual_pool_amount_for_short_token": market_info[5][1],
                "virtual_inventory_for_positions": market_info[5][2],
            },
            "is_disabled": market_info[6]
        }
    
    def get_market_net_funding_rate(self, market):
        '''
        Get net funding rate for a market.

        :param market: required
        :type market: address

        :returns: integer
        ''' 
        market_info = self.get_market_info(market)
        net_funding = market_info["next_funding"]["funding_factor_per_second"]
        direction = -1
        if market_info["next_funding"]["longs_pay_shorts"]:
            direction = 1
        
        net_funding = net_funding * direction
        net_funding = net_funding - market_info["borrowing_factor_per_second_for_shorts"]
        net_funding = net_funding * 60 * 60

        return net_funding

    def get_available_markets(self):
        '''
        Get the available markets for the strategy.

        :returns: []address
        '''
        return self.manager.functions.getAvailableMarkets().call()

    def get_market_configuration(self, market):
        '''
        Get market configuration for the strategy.

        :param market: required
        :type market: address

        :returns: Object
        '''
        return self.manager.functions.getMarketConfiguration(market).call()

    def get_market_unwind_configuration(self, market):
        '''
        Get market unwind configuration for the strategy.

        :param market: required
        :type market: address

        :returns: Object
        '''
        return self.manager.functions.getMarketUnwindConfiguration(market).call()

    def get_is_approved_market(self, market):
        '''
        Get if a market is approved for the strategy.

        :param market: required
        :type market: address

        :returns: boolean
        '''
        return self.manager.functions.isApprovedMarket(market).call()

    # -----------------------------------------------------------
    # Asset Querying Functions
    # -----------------------------------------------------------

    def get_asset_oracle(self, asset):
        '''
        Get the asset oracle for the strategy.

        :param asset: required
        :type asset: address

        :returns: address
        '''
        return self.manager.functions.getAssetOracle(asset).call()

    def get_asset_oracle_configuration(self,  asset):
        '''
        Get the asset oracle configuration for the strategy.

        :param asset: required
        :type asset: address

        :returns: Object
        '''
        return self.manager.functions.getAssetOracleConfiguration(asset).call()

    def get_asset_price(self, asset):
        '''
        Get the asset price for the strategy.

        :param asset: required
        :type asset: address

        :returns: object
        '''
        asset_price = self.manager.functions.getAssetPrice(asset).call()

        return {
            "price": asset_price[0],
            "decimals": asset_price[1],
        }

    def get_registered_assets(self):
        '''
        Get the registered assets for the strategy.

        :returns: []address
        '''
        return self.manager.functions.getRegisteredAssets().call()

    # -----------------------------------------------------------
    # GMX Contract Querying Functions
    # -----------------------------------------------------------

    def get_gmx_v2_exchange_router(self):
        '''
        Get the GMX V2 exchange router for the strategy.

        :returns: address
        '''
        return self.manager.functions.gmxV2ExchangeRouter().call()

    def get_gmx_v2_order_vault(self):
        '''
        Get the GMX V2 order vault for the strategy.

        :returns: address
        '''
        return self.manager.functions.gmxV2OrderVault().call()

    def get_referral_storage(self):
        '''
        Get the referral storage address.

        :return: address
        '''
        return self.manager.functions.gmxV2ReferralStorage().call()

    def get_ui_fee_receiver(self):
        '''
        Get UI fee receiver address.

        :return: address
        '''
        return self.manager.functions.getUiFeeReceiver().call()

    # -----------------------------------------------------------
    # Account Querying Functions
    # -----------------------------------------------------------

    def get_account_orders_value_usd(self, strategy_account):
        '''
        Get an account's order value in USD.

        :param strategy_account: required
        :type strategy_account: address

        :returns: integer
        '''
        return send_raw_query(
            self.web3.provider.endpoint_uri,
            self.account_getters_address,
            "getAccountOrdersValueUSD(IGmxFrfStrategyManager,address)",
            self.manager_address,
            strategy_account,
        )

    def get_account_positions_value_usd(self, strategy_account):
        '''
        Get an account's positions' value in USD.

        :param strategy_account: required
        :type strategy_account: address

        :returns: integer
        '''
        return send_raw_query(
            self.web3.provider.endpoint_uri,
            self.account_getters_address,
            "getAccountPositionsValueUSD(IGmxFrfStrategyManager,address)",
            self.manager_address,
            strategy_account
        )

    def get_account_value_usdc(self, strategy_account):
        '''
        Get an account's value in USDC.

        :param strategy_account: required
        :type strategy_account: address

        :returns: integer
        '''
        return send_raw_query(
            self.web3.provider.endpoint_uri,
            self.account_getters_address,
            "getAccountValueUsdc(IGmxFrfStrategyManager,address)",
            self.manager_address,
            strategy_account
        )

    def get_settled_funding_fees(self, strategy_account, market, short_token, long_token):
        '''
        Get an account's settled funding fees for a market.

        :param strategy_account: required
        :type strategy_account: address

        :param market: required
        :type market: address

        :param short_token: required
        :type short_token: address

        :param long_token: required
        :type long_token: address

        :returns: integer
        '''
        return send_raw_query(
            self.web3.provider.endpoint_uri,
            self.account_getters_address,
            "getSettledFundingFees(IGmxV2DataStore,address,address,address,address)",
            self.data_store_address,
            strategy_account,
            market,
            short_token,
            long_token
        )

    def get_settled_funding_fees_for_token(self, strategy_account, market, token):
        '''
        Get an account's settled funding fees for a token.

        :param strategy_account: required
        :type strategy_account: address

        :param market: required
        :type market: address

        :param token: required
        :type token: address

        :returns: integer
        '''
        key = self.get_claimable_funding_key(market, token, strategy_account)
        return self.igmx_v2_datastore.functions.getUint(key).call()

    def get_settled_funding_fees_value_usd(self, strategy_account):
        '''
        Get an account's settled funding fees total USD value.

        :param strategy_account: required
        :type strategy_account: address

        :returns: integer
        '''
        return send_raw_query(
            self.web3.provider.endpoint_uri,
            self.account_getters_address,
            "getSettledFundingFeesValueUSD(IGmxFrfStrategyManager,address)",
            self.manager_address,
            strategy_account
        )

    def get_is_liquidation_finished(self, strategy_account):
        '''
        Get if an account is not in a liquidation state.

        :param strategy_account: required
        :type strategy_account: address

        :returns: boolean
        '''
        is_finished = send_raw_query(
            self.web3.provider.endpoint_uri,
            self.account_getters_address,
            "isLiquidationFinished(IGmxFrfStrategyManager,address)",
            self.manager_address,
            strategy_account
        )

        return is_finished == 0

    # -----------------------------------------------------------
    # Individual Order/Position Querying Functions
    # -----------------------------------------------------------

    def get_order_value_usd(self, order_id):
        '''
        Get an order's value in USD.

        :param order_id: required
        :type order_id: bytes

        :returns: integer
        '''
        return send_raw_query(
            self.web3.provider.endpoint_uri,
            self.account_getters_address,
            "getOrderValueUSD(IGmxFrfStrategyManager,bytes32)",
            self.manager_address,
            order_id
        )

    def get_position_value_usd(self, strategy_account, market):
        '''
        Get a position's value in USD.

        :param strategy_account: required
        :type strategy_account: address

        :param market: required
        :type market: address

        :returns: integer
        '''
        return send_raw_query(
            self.web3.provider.endpoint_uri,
            self.account_getters_address,
            "getPositionValue(IGmxFrfStrategyManager,address,address)",
            self.manager_address,
            strategy_account,
            market
        )

    def get_position(self, market, strategy_account):
        '''
        Get a position.

        :param market: required
        :type market: address

        :param strategy_account: required
        :type strategy_account: address

        :param market: required
        :type market: address

        :returns: Object
        '''
        position_key = self.get_position_key(market, strategy_account)

        position = self.gmx_v2_reader.functions.getPosition(
            self.data_store_address,
            position_key,
        ).call()

        return {
            "addresses": {
                "account": position[0][0],
                "market": position[0][1],
                "collateral_token": position[0][2],
            },
            "numbers": {
                "size_in_usd": position[1][0],
                "size_in_tokens": position[1][1],
                "collateral_amount": position[1][2],
                "borrowing_factor": position[1][3],
                "funding_fee_amount_per_size": position[1][4],
                "long_token_claimable_funding_amount_per_size": position[1][5],
                "short_token_claimable_funding_amount_per_size": position[1][6],
                "increased_at_block": position[1][7],
                "decreased_at_block": position[1][8],
            },
            "flags": {
                "isLong": position[2][0],
            }
        }

    def get_position_info(self, market, strategy_account):
        '''
        Get a position's info.

        :param market: required
        :type market: address

        :param strategy_account: required
        :type strategy_account: address

        :param market: required
        :type market: address

        :returns: Object
        '''
        market_addresses = self.get_token_addresses_for_market(market)
        short_prices = self.get_asset_price(market_addresses['short_token'])
        long_prices = self.get_asset_price(market_addresses['long_token'])

        position = self.get_position(market, strategy_account)

        position_info = self.gmx_v2_reader.functions.getPositionInfo(
            self.data_store_address,
            self.get_referral_storage(),
            self.get_position_key(market, strategy_account),
            (
                (long_prices["price"], long_prices["price"]),
                (long_prices["price"], long_prices["price"]),
                (short_prices["price"], short_prices["price"]),
            ),
            position["numbers"]["size_in_usd"],
            self.get_ui_fee_receiver(),
            True,
        ).call()

        return {
            "position": {
                "addresses": {
                    "account": position_info[0][0][0],
                    "market": position_info[0][0][1],
                    "collateral_token": position_info[0][0][2],
                },
                "numbers": {
                    "size_in_usd": position_info[0][1][0],
                    "size_in_tokens": position_info[0][1][1],
                    "collateral_amount": position_info[0][1][2],
                    "borrowing_factor": position_info[0][1][3],
                    "funding_fee_amount_per_size": position_info[0][1][4],
                    "long_token_claimable_funding_amount_per_size": position_info[0][1][5],
                    "short_token_claimable_funding_amount_per_size": position_info[0][1][6],
                    "increased_at_block": position_info[0][1][7],
                    "decreased_at_block": position_info[0][1][8],
                },
                "flags": {
                    "isLong": position_info[0][2][0],
                }
            },
            "fees": {
                "referral": {
                    "referral_code": position_info[1][0][0],
                    "affiliate": position_info[1][0][1],
                    "trader": position_info[1][0][2],
                    "total_rebate_factor": position_info[1][0][3],
                    "trader_discount_factor": position_info[1][0][4],
                    "total_rebate_amount": position_info[1][0][5],
                    "trader_discount_amount": position_info[1][0][6],
                    "affiliate_reward_amount": position_info[1][0][7]
                },
                "funding": {
                    "funding_fee_amount": position_info[1][1][0],
                    "claimable_long_token_amount": position_info[1][1][1],
                    "claimable_short_token_amount": position_info[1][1][2],
                    "latest_funding_fee_amount_per_size": position_info[1][1][3],
                    "latest_long_token_claimable_funding_amount_per_size": position_info[1][1][4],
                    "latest_short_token_claimable_funding_amount_per_size": position_info[1][1][5],
                },
                "borrowing": {
                    "borrowing_fee_usd": position_info[1][2][0],
                    "borrowing_fee_amount": position_info[1][2][1],
                    "borrowing_fee_receiver_factor": position_info[1][2][2],
                    "borrowing_fee_amount_for_fee_receiver": position_info[1][2][3],
                },
                "ui": {
                    "ui_fee_receiver": position_info[1][3][0],
                    "ui_fee_receiver_factor": position_info[1][3][1],
                    "ui_fee_amount": position_info[1][3][2],
                },
                "collateral_token_price": {
                    "min": position_info[1][4][0],
                    "max": position_info[1][4][1],
                },
                "position_fee_factor": position_info[1][5],
                "protocol_fee_amount": position_info[1][6],
                "position_fee_receiver_factor": position_info[1][7],
                "fee_receiver_amount": position_info[1][8],
                "fee_amount_for_pool": position_info[1][9],
                "position_fee_amount_for_pool": position_info[1][10],
                "position_fee_amount": position_info[1][11],
                "total_cost_amount_excluding_funding": position_info[1][12],
                "total_cost_amount": position_info[1][13],
            },
            "execution_price_result": {
                "price_impact_usd": position_info[2][0],
                "price_impact_diff_usd": position_info[2][1],
                "execution_price": position_info[2][2],
            },
            "base_pnl_usd": position_info[3],
            "uncapped_base_pnl_usd": position_info[4],
            "pnl_after_price_impact_usd": position_info[5],
        }

    # -----------------------------------------------------------
    # Utility Functions
    # -----------------------------------------------------------

    def get_position_key(self, market, strategy_account):
        '''
        Get a position's key.

        :param market: required
        :type market: address

        :param strategy_account: required
        :type strategy_account: address

        :returns: str
        '''
        market_addresses = self.get_token_addresses_for_market(market)
        return Web3.solidityKeccak(
            ['bytes'],
            [encode_abi(
                ['address', 'address', 'address', 'bool'],
                [strategy_account, market, market_addresses['long_token'], False],
            )],
        ).hex()

    def get_claimable_funding_key(self, market, token, strategy_account):
        '''
        Get a position's claimable funding key.

        :param market: required
        :type market: address

        :param token: required
        :type token: address

        :param strategy_account: required
        :type strategy_account: address

        :returns: str
        '''
        encoded_key = Web3.solidityKeccak(
            ['bytes'],
            [encode_abi(
                ['string'],
                ['CLAIMABLE_FUNDING_AMOUNT'],
            )]
        )

        return Web3.solidityKeccak(
            ['bytes'],
            [encode_abi(
                ['bytes32', 'address', 'address', 'address'],
                [encoded_key, market, token, strategy_account],
            )],
        ).hex()
        