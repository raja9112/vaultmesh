from web3 import Web3
from .base import BaseWalletService

class EVMWalletService(BaseWalletService):
    # todo: Use IPCProvider or WebSocketProvider for better performance in Production
    #       HTTPProvider is suitable for development and testing
    def __init__(self, chain, provider_url):
        self.web3 = Web3(Web3.HTTPProvider(provider_url))
        if not self.web3.is_connected():
            raise ConnectionError(f"Failed to connect to {chain} RPC at {provider_url}")
        else:
            print(f"Connected to {chain} RPC at {provider_url}")

    def create_wallet(self):
        acct = self.web3.eth.account.create()
        return {
        "wallet_format": "EIP-55",
        "address": acct.address,
        "private_key_bytes": acct.key,  # For AES encryption (custodial)
        "private_key_hex": acct.key.hex(),  # For returning in non-custodial
        "public_key_hex": acct._key_obj.public_key.to_hex(),  # Optional
        "chain_id": self.web3.eth.chain_id,
        "network_version": self.web3.net.version,
        "account_type": type(acct).__name__,  # 'LocalAccount'
        "key_obj": acct._key_obj,  # Full crypto object, optional
        "_private_key": acct._private_key,  # Same as acct.key
    }


