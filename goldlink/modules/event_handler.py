"""Module providing access to methods for handling events from GoldLink Contracts."""

class EventHandler(object):

    '''
    Module for handling events from the GoldLink Protocol.
    '''

    def __init__(
            self,
            omnipool,
            prime_broker_manager,
    ):
        self.omnipool = omnipool
        self.prime_broker_manager = prime_broker_manager


    # -----------------------------------------------------------
    # Lending Events
    # -----------------------------------------------------------


    def handle_open_position(self, transaction_receipt):
        '''
        Handle and return event emitted when opening a position.

        :param transaction_receipt: required
        :type transaction_receipt: transactionReceipt

        :returns: AttributeDict
        '''
        return handle_event(self.omnipool.events.OpenPosition().processReceipt(transaction_receipt))
    

    # -----------------------------------------------------------
    # Borrowing Events
    # -----------------------------------------------------------

    def handle_borrow(self, transaction_receipt):
        '''
        Handle and return event emitted when borrowing.

        :param transaction_receipt: required
        :type transaction_receipt: transactionReceipt

        :returns: AttributeDict
        '''
        return handle_event(self.prime_broker_manager.events.Borrow().processReceipt(transaction_receipt))


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
