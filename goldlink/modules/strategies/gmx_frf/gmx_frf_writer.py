"""Module providing access to methods for writing to GoldLink GMX Frf Contracts."""

from goldlink.modules.contract_handler import ContractHandler
from goldlink.modules.transaction_handler import TransactionHandler

class GmxFrfWriter(ContractHandler, TransactionHandler):

    '''
    Module for sending GMX Funding-rate Farming Strategy specific transactions to GoldLink Protocol.
    '''

    def __init__(
        self,
        web3,
        private_key,
        default_address,
        send_options
    ):
        ContractHandler.__init__(self, web3)
        TransactionHandler.__init__(self, web3, private_key, default_address, send_options)

        self.default_address = default_address

    # -----------------------------------------------------------
    # Core Transactions
    # -----------------------------------------------------------

    def create_increase_order(
            self,
            strategy_account,
            market,
            amount,
            send_options=None
    ):
        '''
        Create an increase order for a position.

        :param strategy_account: required
        :type strategy_account: address

        :param market: required
        :type market: address

        :param amount: required
        :type amount: integer

        :param send_options: optional
        :type send_options: sendOptions

        :returns: transactionHash

        :raise: TransactionReverted
        ''' 
        return self.send_transaction(
            method=self.get_gmxfrf_strategy_account(strategy_account).functions.executeCreateIncreaseOrder(
                market=market,
                collateralAmount=amount
            ),
            options=send_options,
        )
    
    def create_decrease_order(
            self,
            strategy_account,
            market,
            size_delta_usd,
            send_options=None
    ):
        '''
        Create a decrease order for a position.

        :param strategy_account: required
        :type strategy_account: address

        :param market: required
        :type market: address

        :param size_delta_usd: required
        :type size_delta_usd: integer

        :param send_options: optional
        :type send_options: sendOptions

        :returns: transactionHash

        :raise: TransactionReverted
        ''' 
        return self.send_transaction(
            method=self.get_gmxfrf_strategy_account(strategy_account).functions.executeCreateDecreaseOrder(
                market=market,
                sizeDeltaUsd=size_delta_usd
            ),
            options=send_options,
        )

    def claim_collateral(
            self,
            strategy_account,
            market,
            asset,
            time_key,
            send_options=None
    ):
        '''
        Claim collateral for a market.

        :param strategy_account: required
        :type strategy_account: address

        :param market: required
        :type market: address

        :param asset: required
        :type asset: address

        :param time_key: required
        :type time_key: integer

        :param send_options: optional
        :type send_options: sendOptions

        :returns: None

        :raise: TransactionReverted
        ''' 
        return self.send_transaction(
            method=self.get_gmxfrf_strategy_account(strategy_account).functions.executeClaimCollateral(
                market=market,
                asset=asset,
                timeKey=time_key
            ),
            options=send_options,
        )
    
    def claim_funding_fees(
            self,
            strategy_account,
            markets,
            assets,
            send_options=None
    ):
        '''
        Claim funding fees across markets.

        :param strategy_account: required
        :type strategy_account: address

        :param markets: required
        :type markets: []address

        :param assets: required
        :type assets: []address
        
        :param send_options: optional
        :type send_options: sendOptions

        :returns: None

        :raise: TransactionReverted
        ''' 
        return self.send_transaction(
            method=self.get_gmxfrf_strategy_account(strategy_account).functions.executeClaimFundingFees(
                markets,
                assets
            ),
            options=send_options,
        )
    
    def cancel_order(
            self,
            strategy_account,
            order_key,
            send_options=None
    ):
        '''
        Cancel an order.

        :param strategy_account: required
        :type strategy_account: address

        :param order_key: required
        :type order_key: bytes

        :param send_options: optional
        :type send_options: sendOptions

        :returns: None

        :raise: TransactionReverted
        ''' 
        return self.send_transaction(
            method=self.get_gmxfrf_strategy_account(strategy_account).functions.executeCancelOrder(
                orderKey=order_key
            ),
            options=send_options,
        )
    
    # -----------------------------------------------------------
    # Liquidation Transactions
    # -----------------------------------------------------------

    def liquidate_assets(
            self,
            strategy_account,
            asset,
            amount,
            callback,
            receiver,
            send_options=None
    ):
        '''
        Liquidate an amount of an asset for an underwater strategy account.

        :param strategy_account: required
        :type strategy_account: address

        :param asset: required
        :type asset: address

        :param amount: required
        :type amount: integer

        :param callback: required
        :type callback: address

        :param receiver: required
        :type receiver: address

        :param send_options: optional
        :type send_options: sendOptions

        :returns: None

        :raise: TransactionReverted
        ''' 
        return self.send_transaction(
            method=self.get_gmxfrf_strategy_account(strategy_account).functions.executeLiquidateAssets(
                asset=asset,
                amount=amount,
                callback=callback,
                receiever=receiver
            ),
            options=send_options,
        )

    def liquidate_position(
            self,
            strategy_account,
            market,
            size_delta_usd,
            send_options=None
    ):
        '''
        Liquidate an amount of a position for an underwater strategy account.

        :param strategy_account: required
        :type strategy_account: address

        :param market: required
        :type market: address

        :param size_delta_usd: required
        :type size_delta_usd: integer

        :param send_options: optional
        :type send_options: sendOptions

        :returns: None

        :raise: TransactionReverted
        ''' 
        return self.send_transaction(
            method=self.get_gmxfrf_strategy_account(strategy_account).functions.executeLiquidatePosition(
                market=market,
                sizeDeltaUsd=size_delta_usd
            ),
            options=send_options,
        )
    
    def rebalance_position(
            self,
            strategy_account,
            market,
            send_options=None
    ):
        '''
        Rebalance a position for a strategy account.

        :param strategy_account: required
        :type strategy_account: address

        :param market: required
        :type market: address

        :param send_options: optional
        :type send_options: sendOptions

        :returns: None

        :raise: TransactionReverted
        ''' 
        return self.send_transaction(
            method=self.get_gmxfrf_strategy_account(strategy_account).functions.executeRebalancePosition(
                market=market
            ),
            options=send_options,
        )
    
    def releverage_position(
            self,
            strategy_account,
            market,
            size_delta_usd,
            send_options=None
    ):
        '''
        Releverage a position for a strategy account.

        :param strategy_account: required
        :type strategy_account: address

        :param market: required
        :type market: address

        :param size_delta_usd: required
        :type size_delta_usd: integer

        :param send_options: optional
        :type send_options: sendOptions

        :returns: None

        :raise: TransactionReverted
        ''' 
        return self.send_transaction(
            method=self.get_gmxfrf_strategy_account(strategy_account).functions.executeReleveragePosition(
                market=market,
                sizeDeltaUsd=size_delta_usd
            ),
            options=send_options,
        )
        
    def swap_rebalance(
            self,
            strategy_account,
            market,
            callback_config,
            send_options=None
    ):
        '''
        Swap rebalance, allowing a liquidator to sell long tokens for USDC.

        :param strategy_account: required
        :type strategy_account: address

        :param market: required
        :type market: address

        :param callback_config: required
        :type callback_config: object

        :param send_options: optional
        :type send_options: sendOptions

        :returns: None

        :raise: TransactionReverted
        ''' 
        return self.send_transaction(
            method=self.get_gmxfrf_strategy_account(strategy_account).functions.executeSwapRebalance(
                market=market,
                callbackConfig=callback_config
            ),
            options=send_options,
        )
    