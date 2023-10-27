"""The GoldLink Client for interacting with the protocol."""

from web3 import Web3

from goldlink.modules.reader import Reader
from goldlink.modules.event_handler import EventHandler
from goldlink.modules.writer import Writer
from goldlink.constants import NETWORK_ID_MAINNET, DEFAULT_API_TIMEOUT
from goldlink.signing.signer import SignWithWeb3, SignWithKey

class Client(object):
    '''
    Client users of the GoldLink-Client-Python will be interacting with the
    GoldLink Protocol through.
    '''

    def __init__(
        self,
        send_options=None,
        api_timeout=None,
        web3=None,
        default_address=None,
        network_id=None,
        private_key=None,
        web3_account=None,
        web3_provider=None,
        host=None,
    ):
        # Set API parameters if input.
        self.send_options = send_options or {}
        self.api_timeout = api_timeout or DEFAULT_API_TIMEOUT

        # Default web3 related parameters to None.
        self.web3 = None
        self.signer = None
        self.network_id = None

        # If web3 or web3 provider, set web3, signer, default address and network id.
        if web3 is not None or web3_provider is not None:
            if isinstance(web3_provider, str):
                web3_provider = Web3.HTTPProvider(
                    web3_provider, request_kwargs={'timeout': self.api_timeout}
                )
            self.web3 = web3 or Web3(web3_provider)
            self.signer = SignWithWeb3(self.web3)
            self.default_address = default_address or self.web3.eth.defaultAccount or None
            self.network_id = self.web3.net.version

        # If a private key was passed in or a web3 account, set signer and default address.
        if private_key is not None or web3_account is not None:
            # May override web3 or web3_provider configuration.
            key = private_key or web3_account.key
            self.signer = SignWithKey(key)
            self.default_address = self.signer.address

        # Make sure web3 is/can be set or revert.
        if not web3 and not host:
            raise Exception(
                'Web3 not passed in and cannot set web3 with no host or web3 provider.'
            )
        self.web3 = web3 or Web3(Web3.HTTPProvider(host))

        # Set default network ID.
        self.network_id = int(
            network_id or self.network_id or NETWORK_ID_MAINNET
        )

        # Initialize the reader and event handler modules. Other modules are initialized on
        # demand, if the necessary configuration options were provided.
        self._reader = Reader(self.web3, self.network_id)
        self._event_handler = EventHandler(self._reader.omnipool, self._reader.prime_broker_manager)
        self._writer = None

    @property
    def reader(self):
        '''
        Get the reader module, used for reading from protocol.
        '''
        return self._reader
    
    @property
    def event_handler(self):
        '''
        Get the event handler module, used for handling events emitted from the protocol.
        '''
        return self._event_handler


    @property
    def writer(self):
        '''
        Get the writer module, used for sending transactions to the protocol.
        '''
        if not self._writer:
            private_key = getattr(self.signer, '_private_key', None)
            if self.web3 and private_key:
                self._writer = Writer(
                    web3=self.web3,
                    omnipool=self.reader.omnipool,
                    prime_broker_manager=self.reader.prime_broker_manager,
                    erc_20_address=self.reader.get_omnipool_allowed_address(),
                    private_key=private_key,
                    default_address=self.default_address,
                    send_options=self.send_options,
                )
            else:
                raise Exception(
                    'Writer module is not supported since neither web3 ' +
                    'nor web3_provider was provided OR since neither ' +
                    'private_key nor web3_account was provided',
                )
        return self._writer
    