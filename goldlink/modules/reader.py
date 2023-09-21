import goldlink.constants as Constants 
from goldlink.modules.contract_handler import ContractHandler

ADDRESS_MANAGER_ABI = 'abi/address-manager.json'

class Reader(ContractHandler):

    def __init__(
        self,
        web3,
        network_id,
    ):
        ContractHandler.__init__(self, web3)
        self.network_id = network_id
        self.address_manager = self.get_contract(self.get_address_manager(), ADDRESS_MANAGER_ABI)

    def get_treasury(self):
        return self.address_manager.functions.treasury().call()

    def get_address_manager(self):
        if self.network_id == Constants.NETWORK_ID_ANVIL:
            return  Constants.ADDRESS_MANAGER_LOCAL

