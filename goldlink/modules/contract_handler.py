"""Module for handling all interactions with GoldLink Contracts."""

import json
import os

import goldlink.constants as Constants

class ContractHandler(object):
    '''
    Generic contract handling contract used by Reader and Writer modules.
    '''

    def __init__(
        self,
        web3,
    ):
        # Set web3.
        self.web3 = web3

        # Initialize empty cached contracts.
        self.cached_contracts = {}
        self.cached_gmx_frf_accounts = {}

    # -----------------------------------------------------------
    # ABI Getter Functions
    # -----------------------------------------------------------
        
    def get_erc20(self, erc20):
        '''
        Get ABI of the ERC20.

        :param erc20: required
        :type erc20: address

        :returns: Object
        '''  
        return self.get_contract(erc20, Constants.ERC20)

    def get_strategy_reserve(self, strategy_reserve):
        '''
        Get ABI of the StrategyReserve.

        :param strategy_reserve: required
        :type strategy_reserve: address

        :returns: Object
        '''
        return self.get_contract(strategy_reserve, Constants.STRATEGY_RESERVE_ABI)
    
    def get_strategy_bank(self, strategy_bank):
        '''
        Get ABI of the StrategyBank.

        :param strategy_bank: required
        :type strategy_bank: address

        :returns: Object
        '''
        return self.get_contract(strategy_bank, Constants.STRATEGY_BANK_ABI)

    def get_strategy_account(self, strategy_account):
        '''
        Get ABI of the StrategyAccount.

        :param strategy_account: required
        :type strategy_account: address

        :returns: Object
        '''
        return self.get_contract(strategy_account, Constants.STRATEGY_ACCOUNT_ABI)
    
    def get_gmxfrf_strategy_account(self, strategy_account):
        '''
        Get ABI of the GmxFrfStrategyAccount.

        :param strategy_account: required
        :type strategy_account: address

        :returns: Object
        '''

        if strategy_account not in self.cached_gmx_frf_accounts and strategy_account in self.cached_contracts:
            del self.cached_contracts[strategy_account]
        
        strategy_obj = self.get_contract(strategy_account, Constants.GMX_FRF_STRATEGY_ACCOUNT_ABI)
        self.cached_gmx_frf_accounts[strategy_account] = strategy_obj

        return strategy_obj
    
    # -----------------------------------------------------------
    # Utility Functions
    # -----------------------------------------------------------

    def create_contract(
        self,
        address,
        file_path,
    ):
        '''
        Create a contract object to allow reading from or writing to a contract
        at a specific address.

        :param address: required
        :type address: string

        :param file_path: required
        :type file_path: string

        :returns: contract

        :raises: FileNotFoundError
        '''
        goldlink_folder = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            '..',
        )
        return self.web3.eth.contract(
            address=address,
            abi=json.load(open(os.path.join(goldlink_folder, file_path), 'r')),
        )

    def get_contract(
        self,
        address,
        file_path,
    ):
        '''
        Fetches or creates a contract object to allow reading from or writing 
        to a contract at a specific address.

        :param address: required
        :type address: string

        :param file_path: required
        :type file_path: string

        :returns: contract

        :raises: FileNotFoundError
        '''
        if address not in self.cached_contracts:
            self.cached_contracts[address] = self.create_contract(
                address,
                file_path,
            )
        return self.cached_contracts[address]
    