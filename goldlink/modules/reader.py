"""Module providing access to methods for reading from GoldLink Contracts."""

import goldlink.constants as Constants
from goldlink.modules.contract_handler import ContractHandler
from goldlink.errors import GoldLinkError

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
        self.prime_broker_manager = self.get_contract(
            self.get_prime_broker_manager(), 
            Constants.PRIME_BROKER_MANAGER_ABI,
        )
        self.strategy_pools = {}
        self.prime_brokers = {}

    # -----------------------------------------------------------
    # Address Querying Functions
    # -----------------------------------------------------------

    def get_address_manager(self):
        '''
        Get address of the Address Manager.

        :returns: address

        :raises: GoldLinkError
        '''
        if self.network_id == Constants.NETWORK_ID_ANVIL:
            return  Constants.CONTRACTS[Constants.ADDRESS_MANAGER][Constants.NETWORK_ID_ANVIL]
        raise GoldLinkError("Invalid network ID")

    def get_omnipool(self):
        '''
        Get address of the OmniPool.

        :returns: address
        '''
        return self.address_manager.functions.omnipool_().call()
    
    def get_prime_broker_manager(self):
        '''
        Get address of the PrimeBrokerManager.

        :returns: address
        '''
        return self.address_manager.functions.primeBrokerManager_().call()

    def get_strategy_pools(self):
        '''
        Get all strategy pool addresses.

        :returns: []address
        '''
        return self.address_manager.functions.getStrategyPools().call()
    
    def get_prime_brokers(self):
        '''
        Get all prime broker addresses.

        :returns: []address
        '''
        return self.address_manager.functions.getPrimeBrokers().call()

    def get_omnipool_allowed_address(self):
        '''
        Get allowed asset address for OmniPool.

        :returns: address
        '''
        return self.omnipool.functions.PROTOCOL_ASSET().call()

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
    # OmniPool Querying Functions
    # -----------------------------------------------------------

    def get_position(self, token_id):
        '''
        Get receipt information for a token.

        :param token_id: required
        :type token_id: integer

        :returns: position
        '''
        return self.omnipool.functions.getPosition(token_id).call()
    
    # -----------------------------------------------------------
    # Prime Broker Querying Functions
    # -----------------------------------------------------------
    
    def get_borrower_holdings(self, prime_broker, borrower):
        '''
        Get borrower holdings in a prime broker. Does not account
        for profit or loss.

        :param prime_broker: required
        :type prime_broker: address

        :param borrower: required
        :type borrower: address

        :returns: BorrowerHoldings
        '''
        if prime_broker not in self.prime_brokers:
            self.prime_brokers[prime_broker] = self.get_contract(
                prime_broker, 
                Constants.PRIME_BROKER_ABI,
            )

        return self.prime_brokers[prime_broker].functions.getBorrowerHoldings(borrower).call()

    def get_health_score(self, prime_broker, borrower_holding):
        '''
        Get borrower holdings health score in a prime broker.

        :param prime_broker: required
        :type prime_broker: address

        :param borrower_holding: required
        :type borrower_holding: BorrowerHoldings

        :returns: integer
        '''
        if prime_broker not in self.prime_brokers:
            self.prime_brokers[prime_broker] = self.get_contract(
                prime_broker, 
                Constants.PRIME_BROKER_ABI,
            )

        return self.prime_brokers[prime_broker].functions.getHealthScore(borrower_holding).call()


    def get_prime_broker_share_price(self, prime_broker):
        '''
        Get prime broker share price.

        :param prime_broker: required
        :type prime_broker: address

        :returns: float
        '''
        if prime_broker not in self.prime_brokers:
            self.prime_brokers[prime_broker] = self.get_contract(
                prime_broker, 
                Constants.PRIME_BROKER_ABI,
            )

        one_thousand_shares_of_asset = self.prime_brokers[prime_broker].functions.convertToAssets(1000).call()
        return one_thousand_shares_of_asset / 1000
