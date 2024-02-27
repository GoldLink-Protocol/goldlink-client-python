"""Module providing access to methods for writing to GoldLink Core Contracts."""

from goldlink.modules.contract_handler import ContractHandler
from goldlink.modules.transaction_handler import TransactionHandler

class Writer(ContractHandler, TransactionHandler):

    '''
    Module for sending non-strategy specific transactions to GoldLink Protocol.
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
    # General Transactions
    # -----------------------------------------------------------

    def approve_address(
            self,
            address,
            amount,
            erc20,
            send_options=None
    ):
        '''
        Approve address to pull allowed asset funds from wallet.

        :param address: required
        :type address: address

        :param amount: required
        :type amount: integer

        :param erc20: required
        :type erc20: address

        :param send_options: optional
        :type send_options: sendOptions

        :returns: transactionHash

        :raises: TransactionReverted
        '''
        return self.send_transaction(
            method=self.get_erc20(erc20).functions.approve(
                address,
                amount
            ),
            options=send_options,
        )
    
    def transfer(
        self,
        to,
        amount,
        erc20,
        send_options=None
    ):
        '''
        Transfer the allowed asset for the GoldLink Protocol to another address.

        :param to: required
        :type to: address

        :param amount: required
        :type amount: integer

        :param erc20: required
        :type erc20: addresss

        :param send_options: optional
        :type send_options: sendOptions

        :returns: transactionHash

        :raises: TransactionReverted
        '''
        return self.send_transaction(
            method=self.get_erc20(erc20).functions.transfer(
                to,
                amount
            ),
            options=send_options,
        )

    # -----------------------------------------------------------
    # Lending Transactions
    # -----------------------------------------------------------

    def deposit(
        self,
        amount,
        strategy_reserve,
        on_behalf_of=None,
        send_options=None
    ):
        '''
        Deposit assets into the strategy reserve and receive tokenized vault shares back.

        :param amount: required
        :type amount: integer

        :param strategy_reserve: required
        :type strategy_reserve: address

        :param on_behalf_of: optional
        :type on_behalf_of: address

        :param send_options: optional
        :type send_options: sendOptions

        :returns: transactionHash

        :raises: TransactionReverted
        '''
        return self.send_transaction(
            method=self.get_strategy_reserve(strategy_reserve).functions.deposit(
                assets=amount,
                receiver=on_behalf_of or self.default_address
            ),
            options=send_options,
        )
    
    def mint(
        self,
        shares,
        strategy_reserve,
        on_behalf_of=None,
        send_options=None
    ):
        '''
        Mint shares in the strategy reserve.

        :param shares: required
        :type shares: integer

        :param strategy_reserve: required
        :type strategy_reserve: address

        :param on_behalf_of: optional
        :type on_behalf_of: address

        :param send_options: optional
        :type send_options: sendOptions

        :returns: transactionHash

        :raises: TransactionReverted
        '''
        return self.send_transaction(
            method=self.get_strategy_reserve(strategy_reserve).functions.mint(
                shares=shares,
                receiver=on_behalf_of or self.default_address
            ),
            options=send_options,
        )

    def withdraw(
        self,
        amount,
        strategy_reserve,
        on_behalf_of=None,
        send_options=None
    ):
        '''
        Withdraw assets from the strategy reserve and burn tokenized vault shares.

        :param amount: required
        :type amount: integer

        :param strategy_reserve: required
        :type strategy_reserve: address

        :param on_behalf_of: optional
        :type on_behalf_of: address

        :param send_options: optional
        :type send_options: sendOptions

        :returns: transactionHash

        :raises: TransactionReverted
        '''
        return self.send_transaction(
            method=self.get_strategy_reserve(strategy_reserve).functions.withdraw(
                assets=amount,
                receiver=on_behalf_of or self.default_address,
                lender=self.default_address
            ),
            options=send_options,
        )
    
    def redeem(
        self,
        shares,
        strategy_reserve,
        on_behalf_of=None,
        send_options=None
    ):
        '''
        Redeem shares from the strategy reserve, withdrawing share value and burning tokenized vault shares.

        :param shares: required
        :type shares: integer

        :param strategy_reserve: required
        :type strategy_reserve: address

        :param on_behalf_of: optional
        :type on_behalf_of: address

        :param send_options: optional
        :type send_options: sendOptions

        :returns: transactionHash

        :raises: TransactionReverted
        '''
        return self.send_transaction(
            method=self.get_strategy_reserve(strategy_reserve).functions.redeem(
                shares=shares,
                receiver=on_behalf_of or self.default_address,
                lender=self.default_address
            ),
            options=send_options,
        )
    
    # -----------------------------------------------------------
    # Borrowing Transactions
    # -----------------------------------------------------------

    def open_account(
        self,
        strategy_bank,
        on_behalf_of=None,
        send_options=None
    ):
        '''
        Open a new strategy account.

        :param strategy_bank: required
        :type strategy_bank: address

        :param on_behalf_of: optional
        :type on_behalf_of: address

        :param send_options: optional
        :type send_options: sendOptions

        :returns: transactionHash

        :raises: TransactionReverted
        '''
        return self.send_transaction(
            method=self.get_strategy_bank(strategy_bank).functions.executeOpenAccount(
                onBehalfOf=on_behalf_of or self.default_address
            ),
            options=send_options,
        )
    
    def add_collateral(
        self,
        strategy_account,
        amount,
        send_options=None
    ):
        '''
        Add collateral to a strategy account.

        :param strategy_account: required
        :type strategy_account: address

        :param amount: required
        :type amount: integer

        :param send_options: optional
        :type send_options: sendOptions

        :returns: transactionHash

        :raise: TransactionReverted
        '''  
        return self.send_transaction(
            method=self.get_strategy_account(strategy_account).functions.executeAddCollateral(
                collateral=amount
            ),
            options=send_options,
        )
    
    def borrow(
        self,
        strategy_account,
        amount,
        send_options=None
    ):
        '''
        Borrow funds into a strategy account.

        :param strategy_account: required
        :type strategy_account: address

        :param amount: required
        :type amount: integer

        :param send_options: optional
        :type send_options: sendOptions

        :returns: transactionHash

        :raise: TransactionReverted
        '''  
        return self.send_transaction(
            method=self.get_strategy_account(strategy_account).functions.executeBorrow(
                loan=amount
            ),
            options=send_options,
        )
    
    def repay(
        self,
        strategy_account,
        amount,
        send_options=None
    ):
        '''
        Repay funds from a strategy account.

        :param strategy_account: required
        :type strategy_account: address

        :param amount: required
        :type amount: integer

        :param send_options: optional
        :type send_options: sendOptions

        :returns: transactionHash

        :raise: TransactionReverted
        '''  
        return self.send_transaction(
            method=self.get_strategy_account(strategy_account).functions.executeRepayLoan(
                repayAmount=amount
            ),
            options=send_options,
        )
    
    def withdraw_collateral(
        self,
        strategy_account,
        amount,
        use_soft_withdrawal=False,
        on_behalf_of=None,
        send_options=None
    ):
        '''
        Withdraw collateral that was put up for a strategy account.

        :param strategy_account: required
        :type strategy_account: address

        :param amount: required
        :type amount: integer

        :param use_soft_withdrawal: optional
        :type use_soft_withdrawal: boolean

        :param on_behalf_of: optional
        :type on_behalf_of: address

        :param send_options: optional
        :type send_options: sendOptions

        :returns: transactionHash

        :raise: TransactionReverted
        '''  
        return self.send_transaction(
            method=self.get_strategy_account(strategy_account).functions.executeWithdrawCollateral(
                onBehalfOf=on_behalf_of or self.default_address,
                collateral=amount,
                useSoftWithdrawal=use_soft_withdrawal
            ),
            options=send_options,
        )

    def withdraw_native_asset(
        self,
        strategy_account,
        amount,
        on_behalf_of=None,
        send_options=None
    ):
        '''
        Withdraw native asset from a strategy account.

        :param strategy_account: required
        :type strategy_account: address

        :param amount: required
        :type amount: integer

        :param on_behalf_of: optional
        :type on_behalf_of: address

        :param send_options: optional
        :type send_options: sendOptions

        :returns: transactionHash

        :raise: TransactionReverted
        '''  
        return self.send_transaction(
            method=self.get_strategy_account(strategy_account).functions.executeWithdrawNativeAsset(
                receiver=on_behalf_of or self.default_address,
                amount=amount
            ),
            options=send_options,
        )
    
    def withdraw_erc20_assets(
        self,
        strategy_account,
        tokens,
        amounts,
        on_behalf_of=None,
        send_options=None
    ):
        '''
        Withdraw erc20 assets from a strategy account.

        :param strategy_account: required
        :type strategy_account: address

        :param tokens: required
        :type tokens: []address

        :param amounts: required
        :type amounts: []integer

        :param on_behalf_of: optional
        :type on_behalf_of: address

        :param send_options: optional
        :type send_options: sendOptions

        :returns: transactionHash

        :raise: TransactionReverted
        '''  
        return self.send_transaction(
            method=self.get_strategy_account(strategy_account).functions.executeWithdrawErc20Assets(
                receiver=on_behalf_of or self.default_address,
                tokens=tokens,
                amounts=amounts
            ),
            options=send_options,
        )
    
    # -----------------------------------------------------------
    # Liquidation Transactions
    # -----------------------------------------------------------

    def initiate_liquidation(
        self,
        strategy_account,
        send_options=None
    ):
        '''
        Initiate a liquidation for a strategy account.

        :param strategy_account: required
        :type strategy_account: address

        :param send_options: optional
        :type send_options: sendOptions

        :returns: transactionHash

        :raise: TransactionReverted
        ''' 
        return self.send_transaction(
            method=self.get_strategy_bank(strategy_account).functions.executeInitiateLiquidation(),
            options=send_options,
        )
    
    def process_liquidation(
        self,
        strategy_account,
        send_options=None
    ):
        '''
        Process a liquidation for a strategy account.

        :param strategy_account: required
        :type strategy_account: address

        :param send_options: optional
        :type send_options: sendOptions

        :returns: transactionHash

        :raise: TransactionReverted
        ''' 
        return self.send_transaction(
            method=self.get_strategy_bank(strategy_account).functions.executeProcessLiquidation(),
            options=send_options,
        )
