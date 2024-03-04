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
        default_address
    ):
        ContractHandler.__init__(self, web3)

        self.network_id = network_id
        self.default_address = default_address

        self.owned_accounts = []

    # -----------------------------------------------------------
    # Address Querying Functions
    # -----------------------------------------------------------
        
    def get_strategy_asset(self, strategy_reserve=None, strategy_bank=None):
        '''
        Get the asset for a strategy.

        :param strategy_reserve: optional
        :type strategy_reserve: address

        :param strategy_bank: optional
        :type strategy_bank: address

        :returns: address
        '''
        if strategy_reserve:
            return  self.get_strategy_reserve(strategy_reserve).functions.STRATEGY_ASSET().call()
        if strategy_bank:
            return  self.get_strategy_bank(strategy_bank).functions.STRATEGY_ASSET().call()

    def get_strategy_bank_for_reserve(self, strategy_reserve):
        '''
        Get address of the StrategyBank for a reserve.

        :param strategy_reserve: required
        :type strategy_reserve: address

        :returns: address
        '''
        return self.get_strategy_reserve(strategy_reserve).functions.STRATEGY_BANK().call()
    
    def get_strategy_reserve_for_bank(self, strategy_bank):
        '''
        Get address of the StrategyReserve for a bank.

        :param strategy_bank: required
        :type strategy_bank: address

        :returns: address
        '''
        return  self.get_strategy_bank(strategy_bank).functions.STRATEGY_RESERVE().call()
    
    def get_strategy_accounts_for_bank(self, strategy_bank, addresss):
        '''
        Get address of every strategy account for a bank.

        :param strategy_bank: required
        :type strategy_bank: address

        :returns: []address
        '''
        strategy_account_address =  self.get_strategy_bank(strategy_bank).functions.STRATEGY_RESERVE().call()

        for strategy_account in strategy_account_address:
           strategy_account_object = self.get_strategy_account(strategy_account)

           if strategy_account_object.functions.getOwner() == addresss or self.default_address:
               self.owned_accounts.push(strategy_account)

        return strategy_account_address

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

    def get_strategy_account_holdings(self, strategy_bank, strategy_account):
        '''
        Get holdings for a strategy account.

        :param strategy_bank: required
        :type strategy_bank: address

        :param strategy_account: address
        :type strategy_account: address

        :returns: AttributeDict
        '''
        holdings = self.get_strategy_bank(strategy_bank).functions.getStrategyAccountHoldings(strategy_account).call()
        return {
            'collateral': holdings[0],
            'loan': holdings[1],
            'interestIndexLast': holdings[2]
        }

    def get_strategy_account_holdings_after_paying_interest(self, strategy_bank, strategy_account):
        '''
        Get holdings for a strategy account after factoring in interest.

        :param strategy_bank: required
        :type strategy_bank: address

        :param strategy_account: address
        :type strategy_account: address

        :returns: AttributeDict
        '''
        holdings = self.get_strategy_bank(strategy_bank).functions.getStrategyAccountHoldingsAfterPayingInterest(strategy_account).call()
        return {
            'collateral': holdings[0],
            'loan': holdings[1],
            'interestIndexLast': holdings[2]
        }

    def get_withdrawable_collateral(self, strategy_bank, strategy_account):
        '''
        Get withdrawable collateral for a strategy account.

        :param strategy_bank: required
        :type strategy_bank: address

        :param strategy_account: address
        :type strategy_account: address

        :returns: integer
        '''
        return self.get_strategy_bank(strategy_bank).functions.getWithdrawableCollateral(strategy_account).call()
