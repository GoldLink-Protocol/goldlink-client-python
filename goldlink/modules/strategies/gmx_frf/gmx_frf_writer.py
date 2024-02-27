"""Module providing access to methods for writing to GoldLink GMX Frf Contracts."""

from goldlink.modules.contract_handler import ContractHandler
from goldlink.modules.transaction_handler import TransactionHandler

class GmxFrfWriter(ContractHandler, TransactionHandler):

    '''
    Module for sending GMX Funding-rate Farming Strategy specific transactions to GoldLink Protocol.
    '''

    def __init__(
        self,
        web3,
        private_key,
        default_address,
        send_options
    ):
        ContractHandler.__init__(self, web3)
        TransactionHandler.__init__(self, web3, private_key, default_address, send_options)

        self.default_address = default_address

    def create_increase_order(
            self,
            strategy_account,
            market,
            amount,
            send_options=None
    ):
        '''
        Create an increase order for a position.

        :param strategy_account: required
        :type strategy_account: address

        :param market: required
        :type market: address

        :param amount: required
        :type amount: integer

        :param send_options: optional
        :type send_options: sendOptions

        :returns: transactionHash

        :raise: TransactionReverted
        ''' 
        return self.send_transaction(
            method=self.get_gmxfrf_strategy_account(strategy_account).functions.executeCreateIncreaseOrder(
                market=market,
                collateralAmount=amount
            ),
            options=send_options,
        )
    