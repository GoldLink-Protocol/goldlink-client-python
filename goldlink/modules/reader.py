import goldlink.constants as Constants
from goldlink.modules.contract_handler import ContractHandler

class Reader(ContractHandler):
    '''
    Module for reading from the GoldLink Protocol.
    '''

    def __init__(
        self,
        web3,
        network_id,
    ):
        ContractHandler.__init__(self, web3)

        self.network_id = network_id

        # Get contracts from ABI.
        self.address_manager = self.get_contract(
            self.get_address_manager(),
            Constants.ADDRESS_MANAGER_ABI,
        )
        self.omnipool = self.get_contract(self.get_omnipool(), Constants.OMNIPOOL_ABI)
        self.nft_manager = self.get_contract(
            self.omnipool.functions.nonfungibleReceiptManager_().call(),
            Constants.NONFUNGIBLE_RECEIPT_MANAGER,
        )

        # Initialize mapping of strategy pool addresses to their contract.
        self.strategy_pools = {}

    # -----------------------------------------------------------
    # Address Querying Functions
    # -----------------------------------------------------------

    def get_address_manager(self):
        '''
        Get address of the Address Manager.

        :returns: string
        '''
        if self.network_id == Constants.NETWORK_ID_ANVIL:
            return  Constants.CONTRACTS[Constants.ADDRESS_MANAGER][Constants.NETWORK_ID_ANVIL]

    def get_omnipool(self):
        '''
        Get address of the OmniPool.

        :returns: string
        '''
        return self.address_manager.functions.omnipool_().call()

    def get_strategy_pools(self):
        '''
        Get all strategy pool addresses.

        :returns: []string
        '''
        return self.address_manager.functions.getStrategyPools().call()

    def get_omnipool_allowed_address(self):
        '''
        Get allowed asset address for OmniPool.

        :returns: string
        '''
        return self.omnipool.functions.allowedAsset_().call()

    # -----------------------------------------------------------
    # Strategy Pool Querying Functions
    # -----------------------------------------------------------

    def get_total_enrolled_funds(self, strategy_pool):
        '''
        Get total enrolled funds in strategy pool.

        :param strategy_pool: required
        :type strategy_pool: string

        :returns: integer
        '''
        # Add `strategy_pool` to `self.strategy_pools` if not a part of the mapping.
        if strategy_pool not in self.strategy_pools:
            self.strategy_pools[strategy_pool] = self.get_contract(
                strategy_pool,
                Constants.STRATEGY_POOL_ABI,
            )

        # Return total enrolled funds for the strategy pool.
        return self.strategy_pools[
            strategy_pool
        ].functions.totalEnrolledFunds_().call()

    # -----------------------------------------------------------
    # Nonfungible Receipt Manager Querying Functions
    # -----------------------------------------------------------

    def get_receipt_information(self, token_id):
        '''
        Get receipt information for a token.

        :param token_id: required
        :type token_id: integer

        :returns: integer
        '''
        return self.nft_manager.functions.getReceipt(token_id).call()
    