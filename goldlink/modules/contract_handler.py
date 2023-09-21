import json
import os

class ContractHandler(object):

    def __init__(
        self, 
        web3,
    ):
        self.web3 = web3
        self.cached_contracts = {}

    def create_contract(
        self,
        address,
        file_path,
    ):
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
        if address not in self.cached_contracts:
            self.cached_contracts[address] = self.create_contract(
                address,
                file_path,
            )
        return self.cached_contracts[address]