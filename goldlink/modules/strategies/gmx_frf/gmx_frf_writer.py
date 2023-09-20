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
        send_options,
        strategy_account=None,
    ):
        ContractHandler.__init__(self, web3)
        TransactionHandler.__init__(
            self,
            web3,
            private_key,
            default_address,
            send_options,
        )

        self.strategy_account = None

        if strategy_account:
            self.set_strategy_account(strategy_account)

    # -----------------------------------------------------------
    # Core Transactions
    # -----------------------------------------------------------

    def create_increase_order(
            self,
            market,
            amount,
            execution_fee,
            send_options=None
    ):
        '''
        Create an increase order for a position.

        :param market: required
        :type market: address

        :param amount: required
        :type amount: integer

        :param execution_fee: required
        :type execution_fee: integer

        :param send_options: optional
        :type send_options: sendOptions

        :returns: transactionHash

        :raise: TransactionReverted
        '''
        return self.send_transaction(
            method=self.strategy_account.functions.executeCreateIncreaseOrder(
                market=market,
                collateralAmount=amount,
                executionFee=execution_fee
            ),
            options=send_options,
        )

    def create_decrease_order(
            self,
            market,
            size_delta_usd,
            execution_fee,
            send_options=None
    ):
        '''
        Create a decrease order for a position.

        :param market: required
        :type market: address

        :param size_delta_usd: required
        :type size_delta_usd: integer

        :param execution_fee: required
        :type execution_fee: integer

        :param send_options: optional
        :type send_options: sendOptions

        :returns: transactionHash

        :raise: TransactionReverted
        '''
        return self.send_transaction(
            method=self.strategy_account.functions.executeCreateDecreaseOrder(
                market=market,
                sizeDeltaUsd=size_delta_usd,
                executionFee=execution_fee
            ),
            options=send_options,
        )

    def claim_collateral(
            self,
            market,
            asset,
            time_key,
            send_options=None
    ):
        '''
        Claim collateral for a market.

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
            method=self.strategy_account.functions.executeClaimCollateral(
                market=market,
                asset=asset,
                timeKey=time_key
            ),
            options=send_options,
        )

    def claim_funding_fees(
            self,
            markets,
            assets,
            send_options=None
    ):
        '''
        Claim funding fees across markets.

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
            method=self.strategy_account.functions.executeClaimFundingFees(
                markets,
                assets
            ),
            options=send_options,
        )

    def cancel_order(
            self,
            order_key,
            send_options=None
    ):
        '''
        Cancel an order.

        :param order_key: required
        :type order_key: bytes

        :param send_options: optional
        :type send_options: sendOptions

        :returns: None

        :raise: TransactionReverted
        '''
        return self.send_transaction(
            method=self.strategy_account.functions.executeCancelOrder(
                orderKey=order_key
            ),
            options=send_options,
        )

    def swap_assets(
            self,
            market,
            long_token_amount_out,
            callback,
            receiver,
            send_options=None
    ):
        '''
        Swap assets for the strategy account.

        :param market: required
        :type market: address

        :param long_token_amount_out: required
        :type long_token_amount_out: integer

        :param callback: required
        :type callback: address

        :param receiver: required
        :type receiver: addresss

        :param send_options: optional
        :type send_options: sendOptions

        :returns: None

        :raise: TransactionReverted
        '''
        return self.send_transaction(
            method=self.strategy_account.functions.executeSwapAssets(
                market=market,
                longTokenAmountOut=long_token_amount_out,
                callback=callback,
                receiver=receiver
            ),
            options=send_options,
        )

    def withdraw_profit(
            self,
            params,
            send_options=None
    ):
        '''
        Withdraw profit from a strategy account.

        :param params: required
        :type params: Object

        :param send_options: optional
        :type send_options: sendOptions

        :returns: None

        :raise: TransactionReverted
        '''
        return self.send_transaction(
            method=self.strategy_account.functions.executeWithdrawProfit(
                params=params
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
            execution_fee,
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

        :param execution_fee: required
        :type execution_fee: integer

        :param send_options: optional
        :type send_options: sendOptions

        :returns: None

        :raise: TransactionReverted
        '''
        return self.send_transaction(
            method=self.get_gmxfrf_strategy_account(strategy_account).functions.executeLiquidatePosition(
                market=market,
                sizeDeltaUsd=size_delta_usd,
                executionFee=execution_fee
            ),
            options=send_options,
        )

    def rebalance_position(
            self,
            strategy_account,
            market,
            execution_fee,
            send_options=None
    ):
        '''
        Rebalance a position for a strategy account.

        :param strategy_account: required
        :type strategy_account: address

        :param market: required
        :type market: address

        :param execution_fee: required
        :type execution_fee: integer

        :param send_options: optional
        :type send_options: sendOptions

        :returns: None

        :raise: TransactionReverted
        '''
        return self.send_transaction(
            method=self.get_gmxfrf_strategy_account(strategy_account).functions.executeRebalancePosition(
                market=market,
                executionFee=execution_fee
            ),
            options=send_options,
        )

    def releverage_position(
            self,
            strategy_account,
            market,
            size_delta_usd,
            execution_fee,
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

        :param execution_fee: required
        :type execution_fee: integer

        :param send_options: optional
        :type send_options: sendOptions

        :returns: None

        :raise: TransactionReverted
        '''
        return self.send_transaction(
            method=self.get_gmxfrf_strategy_account(strategy_account).functions.executeReleveragePosition(
                market=market,
                sizeDeltaUsd=size_delta_usd,
                executionFee=execution_fee
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

    # -----------------------------------------------------------
    # Misc Transactions
    # -----------------------------------------------------------

    def multi_call(
            self,
            data,
            send_options=None
    ):
        '''
        Make a multi-call for the strategy account.

        :param data: required
        :type data: []bytes

        :param send_options: optional
        :type send_options: sendOptions

        :returns: None

        :raise: TransactionReverted
        '''
        return self.send_transaction(
            method=self.strategy_account.functions.multicall(
                data=data
            ),
            options=send_options,
        )

    # -----------------------------------------------------------
    # Utilities
    # -----------------------------------------------------------

    def set_strategy_account(
            self,
            strategy_account
    ):
        '''
        Set strategy account for GMX FRF writer.

        :param strategy_account: required
        :type strategy_account: address
        '''
        self.strategy_account = self.get_gmxfrf_strategy_account(
            strategy_account,
        )
