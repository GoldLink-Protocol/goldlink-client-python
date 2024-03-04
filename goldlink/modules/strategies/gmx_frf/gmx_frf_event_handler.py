"""Module providing access to methods for handling GMX Funding-rate Farming Strategy events from GoldLink Contracts."""

from goldlink.modules.contract_handler import ContractHandler
from goldlink.helpers import handle_event

class GmxFrfEventHandler(ContractHandler):

    '''
    Module for handling events from the GoldLink Protocol for the GMX Funding-rate Farming Strategy strategy.
    '''

    def __init__(
        self,
        web3
    ):
        ContractHandler.__init__(self, web3)

   
    def handle_cancel_order_event(self, strategy_account, transaction_receipt):
        '''
        Handle and return event emitted when canceling an order.

        :param strategy_account: required
        :type strategy_account: address

        :param transaction_receipt: required
        :type transaction_receipt: transactionReceipt

        :returns: AttributeDict
        '''
        strategy_account_abi = self.get_gmxfrf_strategy_account(strategy_account)

        return handle_event(strategy_account_abi.events.CancelOrder().processReceipt(transaction_receipt))

    def handle_claim_collateral_event(self, strategy_account, transaction_receipt):
        '''
        Handle and return event emitted when claiming collateral.

        :param strategy_account: required
        :type strategy_account: address

        :param transaction_receipt: required
        :type transaction_receipt: transactionReceipt

        :returns: AttributeDict
        '''
        strategy_account_abi = self.get_gmxfrf_strategy_account(strategy_account)

        return handle_event(strategy_account_abi.events.ClaimCollateral().processReceipt(transaction_receipt))
    
    def handle_claim_funding_fees_event(self, strategy_account, transaction_receipt):
        '''
        Handle and return event emitted when claiming funding fees.

        :param strategy_account: required
        :type strategy_account: address

        :param transaction_receipt: required
        :type transaction_receipt: transactionReceipt

        :returns: AttributeDict
        '''
        strategy_account_abi = self.get_gmxfrf_strategy_account(strategy_account)

        return handle_event(strategy_account_abi.events.ClaimFundingFees().processReceipt(transaction_receipt))

    def handle_create_decrease_order_event(self, strategy_account, transaction_receipt):
        '''
        Handle and return event emitted when creating a decrease order.

        :param strategy_account: required
        :type strategy_account: address

        :param transaction_receipt: required
        :type transaction_receipt: transactionReceipt

        :returns: AttributeDict
        '''
        strategy_account_abi = self.get_gmxfrf_strategy_account(strategy_account)

        return handle_event(strategy_account_abi.events.CreateDecreaseOrder().processReceipt(transaction_receipt))

    def handle_create_increase_order_event(self, strategy_account, transaction_receipt):
        '''
        Handle and return event emitted when creating an increase order.

        :param strategy_account: required
        :type strategy_account: address

        :param transaction_receipt: required
        :type transaction_receipt: transactionReceipt

        :returns: AttributeDict
        '''
        strategy_account_abi = self.get_gmxfrf_strategy_account(strategy_account)

        return handle_event(strategy_account_abi.events.CreateIncreaseOrder().processReceipt(transaction_receipt))
