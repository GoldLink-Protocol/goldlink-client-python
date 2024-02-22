"""Module providing access to methods for handling events from GoldLink Contracts."""

from goldlink.modules.abi_manager import AbiManager

class EventHandler(object):

    '''
    Module for handling events from the GoldLink Protocol.
    '''

    def __init__(
        self,
        abi_manager: AbiManager
    ):
        self.abi_manager = abi_manager


    # -----------------------------------------------------------
    # Lending Events
    # -----------------------------------------------------------


    def handle_deposit(self, strategy_reserve, transaction_receipt):
        '''
        Handle and return event emitted when opening a position.

        :param strategy_reserve: required
        :type strategy_reserve: address

        :param transaction_receipt: required
        :type transaction_receipt: transactionReceipt

        :returns: AttributeDict
        '''
        strategy_reserve_abi = self.abi_manager.get_strategy_reserve(strategy_reserve)

        return handle_event(strategy_reserve_abi.events.Deposit().processReceipt(transaction_receipt))
    
# -----------------------------------------------------------
# Utilities
# -----------------------------------------------------------

def handle_event(event):
    '''
    Handle parsing a generic event.

    :param event: required
    :type event: Event

    :returns: AttributeDict
    '''
    return event[0]['args']
