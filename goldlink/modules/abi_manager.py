"""Module providing abi management and storage."""

import goldlink.constants as Constants

class AbiManager():
    '''
    Module for managing addres to abi relationships.
    '''

    def __init__(self):
        self.address_to_abi = {}

    # -----------------------------------------------------------
    # ABI Fetchers
    # -----------------------------------------------------------

    def get_strategy_reserve(self, strategy_reserve):
        '''
        Get ABI of the StrategyReserve.

        :param strategy_reserve: required
        :type strategy_reserve: address

        :returns: Object
        '''
        if strategy_reserve not in self.address_to_abi:
            self.address_to_abi[strategy_reserve] = self.get_contract(strategy_reserve, Constants.STRATEGY_RESERVE_ABI)
        return self.address_to_abi[strategy_reserve]
    
    def get_strategy_bank(self, strategy_bank):
        '''
        Get ABI of the StrategyBank.

        :param strategy_bank: required
        :type strategy_bank: address

        :returns: Object
        '''
        if strategy_bank not in self.address_to_abi:
            self.address_to_abi[strategy_bank] = self.get_contract(strategy_bank, Constants.STRATEGY_BANK_ABI)
        return self.address_to_abi[strategy_bank]

    def get_strategy_account(self, strategy_account):
        '''
        Get ABI of the StrategyAccount.

        :param strategy_account: required
        :type strategy_account: address

        :returns: Object
        '''
        if strategy_account not in self.address_to_abi:
            self.address_to_abi[strategy_account] = self.get_contract(strategy_account, Constants.STRATEGY_ACCOUNT_ABI)
        return self.address_to_abi[strategy_account]
    
    def get_erc20(self, erc20):
        '''
        Get ABI of the ERC20.

        :param erc20: required
        :type erc20: address

        :returns: Object
        '''  
        if erc20 not in self.address_to_abi:
            self.address_to_abi[erc20] = self.get_contract(erc20, Constants.ERC20)
        return self.address_to_abi[erc20]
