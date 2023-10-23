"""Module for handling all interactions with GoldLink Contracts."""

import json
import os

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
    