"""Module providing access to methods for reading from GoldLink Contracts for the GMX Funding-rate Farming strategy."""

from goldlink.modules.contract_handler import ContractHandler
from goldlink import constants

class GmxFrfReader(ContractHandler):
    '''
    Module for reading from the GoldLink Protocol for the GMX Funding-rate Farming strategy.
    '''

    def __init__(
        self,
        web3,
        network_id,
        default_address
    ):
        ContractHandler.__init__(self, web3)

        self.network_id = network_id
        self.default_address = default_address

    # -----------------------------------------------------------
    # Strategy Config Querying Functions
    # -----------------------------------------------------------
        
    def get_asset_liquidation_fee_percent(self, strategy_manager, asset):
        '''
        Get the asset liquidation fee percent for the strategy.

        :param strategy_manager: required
        :type strategy_manager: address

        :param asset: required
        :type asset: address

        :returns: integer
        '''
        return self.get_gmxfrf_strategy_manager(strategy_manager).functions.liquidationFeePercent(asset).call()
    
    def get_callback_gas_limit(self, strategy_manager):
        '''
        Get the callback gas limit for the strategy.

        :param strategy_manager: required
        :type strategy_manager: address

        :returns: integer
        '''
        return self.get_gmxfrf_strategy_manager(strategy_manager).functions.getCallbackGasLimit().call()
    
    def get_execution_fee_buffer_percent(self, strategy_manager):
        '''
        Get the execution fee buffer percent for the strategy.

        :param strategy_manager: required
        :type strategy_manager: address

        :returns: integer
        '''
        return self.get_gmxfrf_strategy_manager(strategy_manager).functions.getExecutionFeeBufferPercent().call()
    
    def get_liquidation_order_timeout_deadline(self, strategy_manager):
        '''
        Get the liquidation order timeout deadline for the strategy.

        :param strategy_manager: required
        :type strategy_manager: address

        :returns: integer
        '''
        return self.get_gmxfrf_strategy_manager(strategy_manager).functions.getLiquidationOrderTimeoutDeadline().call()
    
    def get_profit_withdrawal_buffer_percent(self, strategy_manager):
        '''
        Get the profit withdrawal buffer percent for the strategy.

        :param strategy_manager: required
        :type strategy_manager: address

        :returns: integer
        '''
        return self.get_gmxfrf_strategy_manager(strategy_manager).functions.getProfitWithdrawalBufferPercent().call()
    
    def get_referral_code(self, strategy_manager):
        '''
        Get the referral code for the strategy.

        :param strategy_manager: required
        :type strategy_manager: address

        :returns: bytes
        '''
        return self.get_gmxfrf_strategy_manager(strategy_manager).functions.getReferralCode().call()
    
    # -----------------------------------------------------------
    # Market Querying Functions
    # -----------------------------------------------------------

    def get_available_markets(self, strategy_manager):
        '''
        Get the available markets for the strategy.

        :param strategy_manager: required
        :type strategy_manager: address

        :returns: []address
        '''
        return self.get_gmxfrf_strategy_manager(strategy_manager).functions.getAvailableMarkets().call()
    

    def get_market_configuration(self, strategy_manager, market):
        '''
        Get market configuration for the strategy.

        :param strategy_manager: required
        :type strategy_manager: address

        :param market: required
        :type market: address

        :returns: Object
        '''
        return self.get_gmxfrf_strategy_manager(strategy_manager).functions.getMarketConfiguration(market).call()
    
    def get_market_unwind_configuration(self, strategy_manager, market):
        '''
        Get market unwind configuration for the strategy.

        :param strategy_manager: required
        :type strategy_manager: address

        :param market: required
        :type market: address

        :returns: Object
        '''
        return self.get_gmxfrf_strategy_manager(strategy_manager).functions.getMarketUnwindConfiguration(market).call()
    
    def get_is_approved_market(self, strategy_manager, market):
        '''
        Get if a market is approved for the strategy.

        :param strategy_manager: required
        :type strategy_manager: address

        :param market: required
        :type market: address

        :returns: boolean
        '''
        return self.get_gmxfrf_strategy_manager(strategy_manager).functions.isApprovedMarket(market).call()

    # -----------------------------------------------------------
    # Asset Querying Functions
    # -----------------------------------------------------------

    def get_asset_oracle(self, strategy_manager, asset):
        '''
        Get the asset oracle for the strategy.

        :param strategy_manager: required
        :type strategy_manager: address

        :param asset: required
        :type asset: address

        :returns: address
        '''
        return self.get_gmxfrf_strategy_manager(strategy_manager).functions.getAssetOracle(asset).call()

    def get_asset_oracle_configuration(self, strategy_manager, asset):
        '''
        Get the asset oracle configuration for the strategy.

        :param strategy_manager: required
        :type strategy_manager: address

        :param asset: required
        :type asset: address

        :returns: Object
        '''
        return self.get_gmxfrf_strategy_manager(strategy_manager).functions.getAssetOracleConfiguration(asset).call()

    def get_asset_price(self, strategy_manager, asset):
        '''
        Get the asset price for the strategy.

        :param strategy_manager: required
        :type strategy_manager: address

        :param asset: required
        :type asset: address

        :returns: object
        '''
        return self.get_gmxfrf_strategy_manager(strategy_manager).functions.getAssetPrice(asset).call()

    def get_registered_assets(self, strategy_manager):
        '''
        Get the registered assets for the strategy.

        :param strategy_manager: required
        :type strategy_manager: address

        :returns: []address
        '''
        return self.get_gmxfrf_strategy_manager(strategy_manager).functions.getRegisteredAssets().call()

    # -----------------------------------------------------------
    # GMX Contract Querying Functions
    # -----------------------------------------------------------

    def get_gmx_v2_data_store(self, strategy_manager):
        '''
        Get the GMX V2 data store for the strategy.

        :param strategy_manager: required
        :type strategy_manager: address

        :returns: address
        '''
        return self.get_gmxfrf_strategy_manager(strategy_manager).functions.gmxV2DataStore().call()

    def get_gmx_v2_exchange_router(self, strategy_manager):
        '''
        Get the GMX V2 exchange router for the strategy.

        :param strategy_manager: required
        :type strategy_manager: address

        :returns: address
        '''
        return self.get_gmxfrf_strategy_manager(strategy_manager).functions.gmxV2ExchangeRouter().call()

    def get_gmx_v2_order_vault(self, strategy_manager):
        '''
        Get the GMX V2 order vault for the strategy.

        :param strategy_manager: required
        :type strategy_manager: address

        :returns: address
        '''
        return self.get_gmxfrf_strategy_manager(strategy_manager).functions.gmxV2OrderVault().call()
    
    def get_gmx_v2_reader(self, strategy_manager):
        '''
        Get the GMX V2 reader for the strategy.

        :param strategy_manager: required
        :type strategy_manager: address

        :returns: address
        '''
        return self.get_gmxfrf_strategy_manager(strategy_manager).functions.gmxV2Reader().call()

    # -----------------------------------------------------------
    # Account Querying Functions
    # -----------------------------------------------------------

    def get_account_liquidation_status(self, strategy_account):
        '''
        Get an account's liquidation status.

        :param strategy_account: required
        :type strategy_account: address

        :returns: integer, 0 == not liquidatable
        '''
        return self.get_gmxfrf_strategy_account(strategy_account).functions.getAccountLiquidationStatus().call()

    def get_account_orders_value_usd(self, account_getters, strategy_manager, strategy_account):
        '''
        Get an account's order value in USD.

        :param account_getters: required
        :type account_getters: address

        :param strategy_manager: required
        :type strategy_manager: address

        :param strategy_account: required
        :type strategy_account: address

        :returns: integer
        '''
        return self.get_gmxfrf_account_getters(account_getters).functions.getAccountOrdersValueUSD(strategy_manager, strategy_account).call()

    def get_account_positions_value_usd(self, account_getters, strategy_manager, strategy_account):
        '''
        Get an account's positions' value in USD.

        :param account_getters: required
        :type account_getters: address

        :param strategy_manager: required
        :type strategy_manager: address

        :param strategy_account: required
        :type strategy_account: address

        :returns: integer
        '''
        return self.get_gmxfrf_account_getters(account_getters).functions.getAccountPositionsValueUSD(strategy_manager, strategy_account).call()

    def get_settled_funding_fees(
            self, 
            account_getters, 
            data_store, 
            strategy_account, 
            market, 
            short_token,
            long_token,
        ):
        '''
        Get an account's settled funding fees for a market

        :param account_getters: required
        :type account_getters: address

        :param data_store: required
        :type data_store: address
        
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
        return self.get_gmxfrf_account_getters(account_getters).functions.getSettledFundingFees(
            dataStore=data_store,
            account=strategy_account,
            market=market,
            shortToken=short_token,
            longToken=long_token
        )
