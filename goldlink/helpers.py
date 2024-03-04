def handle_event(event):
    '''
    Handle parsing a generic event.

    :param event: required
    :type event: Event

    :returns: AttributeDict
    '''
    return event[0]['args']
