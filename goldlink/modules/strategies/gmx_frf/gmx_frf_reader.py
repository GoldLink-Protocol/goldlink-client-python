"""Module providing access to methods for reading from GoldLink Contracts for the GMX Funding-rate Farming strategy."""

from goldlink.modules.contract_handler import ContractHandler
from goldlink.helpers import send_raw_query
from goldlink.modules.strategies.gmx_frf.constants import CONTRACTS, ACCOUNT_GETTERS, MANAGER, DATA_STORE

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
        self.manager_address = CONTRACTS[MANAGER][self.network_id]
        self.data_store_address = CONTRACTS[DATA_STORE][self.network_id]

        # Set strategy specific contracts.
        self.manager =self.get_gmxfrf_strategy_manager(self.manager_address) 

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

    def get_asset_oracle(self,asset):
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
        return self.manager.functions.getAssetPrice(asset).call()

    def get_registered_assets(self):
        '''
        Get the registered assets for the strategy.

        :returns: []address
        '''
        return self.manager.functions.getRegisteredAssets().call()

    # -----------------------------------------------------------
    # GMX Contract Querying Functions
    # -----------------------------------------------------------

    def get_gmx_v2_data_store(self):
        '''
        Get the GMX V2 data store for the strategy.

        :returns: address
        '''
        return self.manager.functions.gmxV2DataStore().call()

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
    
    def get_gmx_v2_reader(self):
        '''
        Get the GMX V2 reader for the strategy.

        :returns: address
        '''
        return self.manager.functions.gmxV2Reader().call()

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
            strategy_account
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

    def get_settled_funding_fees(
            self, 
            strategy_account, 
            market, 
            short_token,
            long_token,
        ):
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

        :returns: Object
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
    
    def get_settled_funding_fees_value_usd(
            self, 
            strategy_account
        ):
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
        is_finished =  send_raw_query(
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
