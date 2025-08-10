from django.test import TestCase
from web3 import Web3
from decouple import config

def get_web3_client(chain: str) -> Web3:
    rpc_url = f'https://sepolia.infura.io/v3/{config("ETH_RPC_API")}'
    web3 = Web3(Web3.HTTPProvider(rpc_url))
    
    if not web3.is_connected():
        raise ConnectionError(f"Failed to connect to {chain} RPC at {rpc_url}")
    
    return web3

print(get_web3_client("ETH"))  

