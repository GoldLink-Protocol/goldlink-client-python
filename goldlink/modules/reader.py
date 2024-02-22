"""Module providing access to methods for reading from GoldLink Contracts."""

from goldlink.modules.contract_handler import ContractHandler
from goldlink.modules.abi_manager import AbiManager

class Reader(ContractHandler):
    '''
    Module for reading from the GoldLink Protocol.
    '''

    def __init__(
        self,
        web3,
        network_id,
        address,
        abi_manager: AbiManager
    ):
        ContractHandler.__init__(self, web3)

        self.network_id = network_id
        self.address = address
        self.abi_manager = abi_manager

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
            return  self.abi_manager.get_strategy_reserve(strategy_reserve).functions.STRATEGY_ASSET().call()
        if strategy_bank:
            return  self.abi_manager.get_strategy_bank(strategy_bank).functions.STRATEGY_ASSET().call()

    def get_strategy_bank_for_reserve(self, strategy_reserve):
        '''
        Get address of the StrategyBank for a reserve.

        :param strategy_reserve: required
        :type strategy_reserve: address

        :returns: address
        '''
        return self.abi_manager.get_strategy_reserve(strategy_reserve).functions.STRATEGY_BANK().call()
    
    def get_strategy_reserve_for_bank(self, strategy_bank):
        '''
        Get address of the StrategyReserve for a bank.

        :param strategy_bank: required
        :type strategy_bank: address

        :returns: address
        '''
        return  self.abi_manager.get_strategy_bank(strategy_bank).functions.STRATEGY_RESERVE().call()
    
    def get_strategy_accounts_for_bank(self, strategy_bank):
        '''
        Get address of every strategy account for a bank.

        :param strategy_bank: required
        :type strategy_bank: address

        :returns: []address
        '''
        strategy_account_address =  self.abi_manager.get_strategy_bank(strategy_bank).functions.STRATEGY_RESERVE().call()

        for strategy_account in strategy_account_address:
           strategy_account_object = self.abi_manager.get_strategy_account(strategy_account)

           if strategy_account_object.functions.getOwner() == self.address:
               self.owned_accounts.push(strategy_account)

        return strategy_account_address
