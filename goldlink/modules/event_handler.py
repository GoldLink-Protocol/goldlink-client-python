"""Module providing access to methods for handling events from GoldLink Contracts."""

from goldlink.modules.contract_handler import ContractHandler

class EventHandler(ContractHandler):

    '''
    Module for handling events from the GoldLink Protocol.
    '''

    def __init__(
        self,
        web3
    ):
        ContractHandler.__init__(self, web3)

    # -----------------------------------------------------------
    # Lending Events
    # -----------------------------------------------------------

    def handle_deposit_event(self, strategy_reserve, transaction_receipt):
        '''
        Handle and return event emitted when depositing into a strategy reserve.

        :param strategy_reserve: required
        :type strategy_reserve: address

        :param transaction_receipt: required
        :type transaction_receipt: transactionReceipt

        :returns: AttributeDict
        '''
        strategy_reserve_abi = self.get_strategy_reserve(strategy_reserve)

        return handle_event(strategy_reserve_abi.events.Deposit().processReceipt(transaction_receipt))
    
    def handle_withdraw_event(self, strategy_reserve, transaction_receipt):
        '''
        Handle and return event emitted when withdrawing from a strategy reserve.

        :param strategy_reserve: required
        :type strategy_reserve: address

        :param transaction_receipt: required
        :type transaction_receipt: transactionReceipt

        :returns: AttributeDict
        '''
        strategy_reserve_abi = self.get_strategy_reserve(strategy_reserve)

        return handle_event(strategy_reserve_abi.events.Withdraw().processReceipt(transaction_receipt))
    
    # -----------------------------------------------------------
    # Borrowing Events
    # -----------------------------------------------------------

    def handle_open_account_event(self, strategy_bank, transaction_receipt):
        '''
        Handle and return event emitted when opening a strategy account.

        :param strategy_bank: required
        :type strategy_bank: address

        :param transaction_receipt: required
        :type transaction_receipt: transactionReceipt

        :returns: AttributeDict
        '''
        strategy_bank_abi = self.get_strategy_bank(strategy_bank)

        return handle_event(strategy_bank_abi.events.OpenAccount().processReceipt(transaction_receipt))
    
    def handle_add_collateral_event(self, strategy_bank, transaction_receipt):
        '''
        Handle and return event emitted when adding collateral to a strategy account.

        :param strategy_bank: required
        :type strategy_bank: address

        :param transaction_receipt: required
        :type transaction_receipt: transactionReceipt

        :returns: AttributeDict
        '''
        strategy_bank_abi = self.get_strategy_bank(strategy_bank)

        return handle_event(strategy_bank_abi.events.AddCollateral().processReceipt(transaction_receipt))

    def handle_borrow_event(self, strategy_bank, transaction_receipt):
        '''
        Handle and return event emitted when borrowing into a strategy account.

        :param strategy_bank: required
        :type strategy_bank: address

        :param transaction_receipt: required
        :type transaction_receipt: transactionReceipt

        :returns: AttributeDict
        '''
        strategy_bank_abi = self.get_strategy_bank(strategy_bank)

        return handle_event(strategy_bank_abi.events.BorrowFunds().processReceipt(transaction_receipt))
    
    def handle_repay_event(self, strategy_bank, transaction_receipt):
        '''
        Handle and return event emitted when repaying from a strategy account.

        :param strategy_bank: required
        :type strategy_bank: address

        :param transaction_receipt: required
        :type transaction_receipt: transactionReceipt

        :returns: AttributeDict
        '''
        strategy_bank_abi = self.get_strategy_bank(strategy_bank)

        return handle_event(strategy_bank_abi.events.RepayLoan().processReceipt(transaction_receipt))

    def handle_withdraw_collateral_event(self, strategy_bank, transaction_receipt):
        '''
        Handle and return event emitted when withdrawing collateral from a strategy account.

        :param strategy_bank: required
        :type strategy_bank: address

        :param transaction_receipt: required
        :type transaction_receipt: transactionReceipt

        :returns: AttributeDict
        '''
        strategy_bank_abi = self.get_strategy_bank(strategy_bank)

        return handle_event(strategy_bank_abi.events.WithdrawCollateral().processReceipt(transaction_receipt))

    def handle_withdraw_native_asset_event(self, strategy_account, transaction_receipt):
        '''
        Handle and return event emitted when withdrawing the native asset from a strategy account.

        :param strategy_account: required
        :type strategy_account: address

        :param transaction_receipt: required
        :type transaction_receipt: transactionReceipt

        :returns: AttributeDict
        '''
        strategy_account_abi = self.get_strategy_account(strategy_account)

        return handle_event(strategy_account_abi.events.WithdrawNativeAsset().processReceipt(transaction_receipt))

    def handle_withdraw_erc20_assets_event(self, strategy_account, transaction_receipt):
        '''
        Handle and return event emitted when withdrawing erc20 balances from a strategy account.

        :param strategy_account: required
        :type strategy_account: address

        :param transaction_receipt: required
        :type transaction_receipt: transactionReceipt

        :returns: AttributeDict
        '''
        strategy_account_abi = self.get_strategy_account(strategy_account)

        return handle_event(strategy_account_abi.events.WithdrawErc20Asset().processReceipt(transaction_receipt))

    # -----------------------------------------------------------
    # Liquidation Events
    # -----------------------------------------------------------

    def handle_initiate_liquidation_event(self, strategy_account, transaction_receipt):
        '''
        Handle and return event emitted when initiating a liquidation for a strategy account.

        :param strategy_account: required
        :type strategy_account: address

        :param transaction_receipt: required
        :type transaction_receipt: transactionReceipt

        :returns: AttributeDict
        '''
        strategy_account_abi = self.get_strategy_account(strategy_account)

        return handle_event(strategy_account_abi.events.InitiateLiquidation().processReceipt(transaction_receipt))

    def handle_liquidate_loan_event(self, strategy_bank, transaction_receipt):
        '''
        Handle and return event emitted when liquidating a loan for a strategy account.

        :param strategy_bank: required
        :type strategy_bank: address

        :param transaction_receipt: required
        :type transaction_receipt: transactionReceipt

        :returns: AttributeDict
        '''
        strategy_bank_abi = self.get_strategy_bank(strategy_bank)

        return handle_event(strategy_bank_abi.events.LiquidateLoan().processReceipt(transaction_receipt))

    def handle_process_liquidation_event(self, strategy_account, transaction_receipt):
        '''
        Handle and return event emitted when processing a liquidation for a strategy account.

        :param strategy_account: required
        :type strategy_account: address

        :param transaction_receipt: required
        :type transaction_receipt: transactionReceipt

        :returns: AttributeDict
        '''
        strategy_account_abi = self.get_strategy_account(strategy_account)

        return handle_event(strategy_account_abi.events.ProcessLiquidation().processReceipt(transaction_receipt))

# -----------------------------------------------------------
# Utilities
# -----------------------------------------------------------

def handle_event(event):
    '''
    Handle parsing a generic event.

    :param event: required
    :type event: Event

    :returns: AttributeDict
    '''
    return event[0]['args']
