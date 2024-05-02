"""Module providing access to methods for reading from GoldLink Contracts."""

from goldlink.modules.contract_handler import ContractHandler

class Reader(ContractHandler):
    '''
    Module for reading from the GoldLink Protocol.
    '''

    def __init__(
        self,
        web3,
        network_id,
        strategy_bank=None,
        strategy_reserve=None,
    ):
        ContractHandler.__init__(self, web3)

        self.network_id = network_id

        self.strategy_bank = None
        self.strategy_reserve = None

        if strategy_bank:
            self.strategy_bank = self.get_strategy_bank(strategy_bank)
        if strategy_reserve:
            self.strategy_reserve = self.get_strategy_reserve(strategy_reserve)

    # -----------------------------------------------------------
    # Address Querying Functions
    # -----------------------------------------------------------
        
    def get_strategy_asset(self):
        '''
        Get the asset for a strategy.

        :returns: address
        '''
        if self.strategy_reserve:
            return  self.strategy_reserve.functions.STRATEGY_ASSET().call()
        if self.strategy_bank:
            return  self.strategy_bank.functions.STRATEGY_ASSET().call()

    def get_strategy_bank_for_reserve(self):
        '''
        Get address of the StrategyBank for a reserve.

        :returns: address
        '''
        return self.strategy_reserve.functions.STRATEGY_BANK().call()
    
    def get_strategy_reserve_for_bank(self):
        '''
        Get address of the StrategyReserve for a bank.

        :returns: address
        '''
        return  self.strategy_bank.functions.STRATEGY_RESERVE().call()

    # -----------------------------------------------------------
    # ERC20 Querying Functions
    # -----------------------------------------------------------

    def get_balance_of(self, erc20, address):
        '''
        Get address balance of erc20.

        :param erc20: required
        :type erc20: address

        :param address: address
        :type address: address

        :returns: integer
        '''
        return self.get_erc20(erc20).functions.balanceOf(address).call()
    
    # -----------------------------------------------------------
    # Borrowing Functions
    # -----------------------------------------------------------

    def get_strategy_accounts_for_bank(self, owner=None):
        '''
        Get address of every strategy account for a bank or just owned by `owner`.

        :param owner: optional
        :type owner: address

        :returns: []address
        '''
        strategy_account_addresses = self.strategy_bank.functions.getStrategyAccounts(0,0).call()

        if owner:
            strategy_account_addresses = [s for s in strategy_account_addresses if self.get_strategy_account(s).functions.getOwner().call() == owner]

        return strategy_account_addresses

    def get_strategy_account_holdings(self, strategy_account):
        '''
        Get holdings for a strategy account.

        :param strategy_account: address
        :type strategy_account: address

        :returns: AttributeDict
        '''
        holdings = self.strategy_bank.functions.getStrategyAccountHoldings(strategy_account).call()
        return {
            'collateral': holdings[0],
            'loan': holdings[1],
            'interestIndexLast': holdings[2]
        }

    def get_strategy_account_holdings_after_paying_interest(self, strategy_account):
        '''
        Get holdings for a strategy account after factoring in interest.

        :param strategy_account: address
        :type strategy_account: address

        :returns: AttributeDict
        '''
        holdings = self.strategy_bank.functions.getStrategyAccountHoldingsAfterPayingInterest(strategy_account).call()
        return {
            'collateral': holdings[0],
            'loan': holdings[1],
            'interestIndexLast': holdings[2]
        }

    def get_withdrawable_collateral(self, strategy_account):
        '''
        Get withdrawable collateral for a strategy account.

        :param strategy_account: address
        :type strategy_account: address

        :returns: integer
        '''
        return self.strategy_bank.functions.getWithdrawableCollateral(strategy_account).call()

    def get_account_liquidation_status(self, strategy_account):
        '''
        Get account liquidation status.

        :param strategy_account: address
        :type strategy_account: address

        :returns: integer, 0 == not liquidatable
        '''
        return self.get_strategy_account(strategy_account).functions.getAccountLiquidationStatus().call()

    def get_account_value(self, strategy_account):
        '''
        Get account value.

        :param strategy_account: address
        :type strategy_account: address

        :returns: integer
        '''
        return self.get_strategy_account(strategy_account).functions.getAccountValue().call()
