from web3 import AsyncWeb3

from goldlink.modules.reader import Reader

class Client(object):

    def __init__(
        self,
        network_id,
        host=None,
        web3=None,
        # default_ethereum_address=None,
        # eth_private_key=None,
        # web3_account=None,
    ):
        self.network_id = network_id
        self.web3 = web3 or AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(host))
        self.default_address = self.web3.eth.default_account or None

        self._reader = Reader(web3, network_id)

    @property
    def reader(self):
        '''
        Get the reader module, used for reading from protocol.
        '''
        return self._reader
