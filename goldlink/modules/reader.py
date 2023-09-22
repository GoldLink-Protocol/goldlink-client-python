import goldlink.constants as Constants 
from goldlink.modules.contract_handler import ContractHandler

ADDRESS_MANAGER_ABI = 'abi/address-manager.json'
OMNIPOOL_ABI = 'abi/omnipool.json'
STRATEGY_POOL_ABI = 'abi/strategy-pool.json'

class Reader(ContractHandler):

    def __init__(
        self,
        web3,
        network_id,
    ):
        ContractHandler.__init__(self, web3)
        self.network_id = network_id
        self.address_manager = self.get_contract(self.get_address_manager(), ADDRESS_MANAGER_ABI)
        self.omnipool = self.get_contract(self.get_omnipool(), OMNIPOOL_ABI)
        self.strategy_pools = {}

    # -----------------------------------------------------------
    # Address Querying Functions
    # -----------------------------------------------------------    

    def get_treasury(self):
        return self.address_manager.functions.treasury().call()
    
    def get_omnipool(self):
        return self.address_manager.functions.omnipool().call()
    
    def get_omnipool_allowed_address(self):
        return self.omnipool.functions.allowedAsset().call()
    
    def get_prime_broker_manager(self):
        return self.address_manager.functions.primeBrokerManager().call()
    
    def get_strategies(self):
        return self.address_manager.functions.getStrategyPools().call()

    def get_address_manager(self):
        if self.network_id == Constants.NETWORK_ID_ANVIL:
            return  Constants.ADDRESS_MANAGER_ANVIL


    # -----------------------------------------------------------
    # Strategy Pool Querying Functions
    # -----------------------------------------------------------    

    def get_total_enrolled_funds(self, strategyPool):
        if strategyPool not in self.strategy_pools:
            self.strategy_pools[strategyPool] = self.get_contract(strategyPool, STRATEGY_POOL_ABI)
        return self.strategy_pools[strategyPool].functions.totalEnrolledFunds().call()
    