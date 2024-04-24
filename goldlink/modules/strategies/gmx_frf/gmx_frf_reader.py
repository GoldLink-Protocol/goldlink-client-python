"""Module providing access to methods for reading from GoldLink Contracts for the GMX Funding-rate Farming strategy."""

from goldlink.modules.contract_handler import ContractHandler

class GmxFrfReader(ContractHandler):
    '''
    Module for reading from the GoldLink Protocol for the GMX Funding-rate Farming strategy.
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

    # -----------------------------------------------------------
    # Strategy Config Querying Functions
    # -----------------------------------------------------------
        
    def get_asset_liquidation_fee_percent(self, strategy_manager, asset):
        '''
        Get the asset liquidation fee percent for the strategy.

        :param strategy_manager: required
        :type strategy_manager: address

        :param asset: required
        :type asset: address

        :returns: integer
        '''
        return self.get_gmxfrf_strategy_manager(strategy_manager).functions.liquidationFeePercent(asset).call()
