from goldlink import constants

# ============ Signature Helpers ============


def is_valid_sig_type(
    sig_type,
):
    '''
    Return if signature type is valid.

    :param sig_type: required
    :type sig_type: integer

    :returns: boolean
    '''
    return sig_type in [
        constants.SIGNATURE_TYPE_DECIMAL,
        constants.SIGNATURE_TYPE_HEXADECIMAL,
        constants.SIGNATURE_TYPE_NO_PREPEND,
    ]


def create_typed_signature(
    signature,
    sig_type,
):
    '''
    Convert raw signature to typed signature.

    :param signature: required
    :type signature: string

    :param sig_type: required
    :type sig_type: integer

    :returns: string
    '''
    if not is_valid_sig_type(sig_type):
        raise Exception('Invalid signature type: ' + sig_type)

    return fix_raw_signature(signature) + '0' + str(sig_type)


def fix_raw_signature(
    signature,
):
    '''
    Fix raw signature by prepending and appending so that it can become
    a typed signature.

    :param signature: required
    :type signature: string

    :returns: string
    '''
    stripped = strip_hex_prefix(signature)

    # Verify stripped signature is the right length.
    if len(stripped) != 130:
        raise Exception('Invalid raw signature: ' + signature)

    rs = stripped[:128]
    v = stripped[128: 130]

    if v == '00':
        return '0x' + rs + '1b'
    if v == '01':
        return '0x' + rs + '1c'
    if v in ['1b', '1c']:
        return '0x' + stripped

    raise Exception('Invalid v value: ' + v)

# ============ Byte Helpers ============


def strip_hex_prefix(signature):
    '''
    Remove hex prefix from input if it is present.

    :param signature: required
    :type signature: string

    :returns: string
    '''
    if signature.startswith('0x'):
        return signature[2:]

    return signature
