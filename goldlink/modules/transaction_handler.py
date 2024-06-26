"""Module providing access to sending and handling transactions for the GoldLink Contracts."""

import goldlink.constants as Constants
from goldlink.errors import TransactionReverted


class TransactionHandler():

    '''
    Module for sending transactions to GoldLink Protocol.
    '''

    def __init__(
        self,
        web3,
        private_key,
        default_address,
        send_options
    ):
        self.web3 = web3
        self.private_key = private_key
        self.default_address = default_address
        self.send_options = send_options

        # Initialize mapping of next nonce per address.
        self._next_nonce_for_address = {}

    def send_transaction(
        self,
        method=None,
        options=None,
    ):
        '''
        Get the next nonce for the address.

        :param method: optional
        :type method: function

        :param options: optional
        :type options: transactionOptions

        :returns: hex

        :raises: ValueError
        '''
        options = dict(self.send_options, **(options or {}))

        # Set from in options.
        if 'from' not in options:
            options['from'] = self.default_address
        if options.get('from') is None:
            raise ValueError(
                "options['from'] is not set, and no default address is set",
            )
        # Set nonce in options.
        auto_detect_nonce = 'nonce' not in options
        if auto_detect_nonce:
            options['nonce'] = self.get_next_nonce(options['from'])

        # Set gas price in options.
        if 'gasPrice' not in options:
            try:
                options['gasPrice'] = (
                    self.web3.eth.gasPrice + Constants.DEFAULT_GAS_PRICE_ADDITION
                )
            except Exception:
                options['gasPrice'] = Constants.DEFAULT_GAS_PRICE

        # Set value in options.
        if 'value' not in options:
            options['value'] = 0

        # Set gas in options.
        gas_multiplier = options.pop(
            'gasMultiplier',
            Constants.DEFAULT_GAS_MULTIPLIER,
        )
        if 'gas' not in options:
            try:
                options['gas'] = int(
                    method.estimateGas(options) * gas_multiplier
                )
            except Exception:
                options['gas'] = Constants.DEFAULT_GAS_AMOUNT

        # Sign and send transaction.
        signed = self.sign_transaction(method, options)
        try:
            transaction_hash = self.web3.eth.sendRawTransaction(
                signed.rawTransaction,
            )
        except ValueError as error:
            # Try to resend with higher nonce if nonce is too low.
            while (
                auto_detect_nonce and
                (
                    'nonce too low' in str(error) or
                    'replacement transaction underpriced' in str(error)
                )
            ):
                try:
                    options['nonce'] += 1
                    signed = self.sign_transaction(method, options)
                    transaction_hash = self.web3.eth.sendRawTransaction(
                        signed.rawTransaction,
                    )
                except ValueError as inner_error:
                    error = inner_error
                else:
                    break  # Break on success...
            else:
                raise error  # ...and raise error otherwise.

        # Update next nonce for the account.
        self._next_nonce_for_address[options['from']] = options['nonce'] + 1

        # Return hex of transaction hash.
        return transaction_hash.hex()

    def get_next_nonce(
        self,
        address,
    ):
        '''
        Get the next nonce for the address.

        :param method: required
        :type method: function

        :param address: required
        :type address: string

        :returns: integer

        :raises: TransactionReverted
        '''
        if self._next_nonce_for_address.get(address) is None:
            self._next_nonce_for_address[address] = (
                self.web3.eth.getTransactionCount(address)
            )
        return self._next_nonce_for_address[address]

    def sign_transaction(
        self,
        method,
        options,
    ):
        '''
        Sign contract call with private key.

        :param method: required
        :type method: function

        :param options: required
        :type options: transactionOptions

        :returns: signedTransaction

        :raises: TransactionReverted
        '''
        transaction = method.build_transaction(options)
        return self.web3.eth.account.signTransaction(
            transaction,
            self.private_key,
        )

    def wait_for_transaction(
        self,
        transaction_hash,
    ):
        '''
        Wait for a transaction to be mined and return the receipt.
        Raise on revert.

        :param transaction_hash: required
        :type transaction_hash: number

        :returns: transactionReceipt

        :raises: TransactionReverted
        '''
        transaction_receipt = self.web3.eth.waitForTransactionReceipt(
            transaction_hash,
        )
        if transaction_receipt['status'] == 0:
            raise TransactionReverted(transaction_receipt)

        return transaction_receipt
