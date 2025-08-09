from .evm_chain_service import EVMWalletService
from decouple import config


class WalletServiceFactory:
    EVM_RPC_URLS = {
        # "ETH": f'https://mainnet.infura.io/v3/{config("ETH_MAINNET_RPC_API")}',     For mainnet 
        "ETH": f'https://sepolia.infura.io/v3/{config("ETH_RPC_API")}',     # For testnet
        "BSC": f'https://rpc.ankr.com/bsc_testnet_chapel/{config("RPC_TESTNET_API")}',
        "POLYGON": f'https://rpc.ankr.com/polygon_amoy/{config("RPC_TESTNET_API")}',
        "AVALANCHE": f'https://rpc.ankr.com/avalanche_fuji-c/{config("RPC_TESTNET_API")}',
    }

    @staticmethod
    def get_rpc_url(chain):
        try:
            return WalletServiceFactory.EVM_RPC_URLS[chain.upper()]
        except KeyError:
            raise NotImplementedError(f"RPC URL for {chain} not configured")

    @staticmethod
    def get_service(chain : str) -> str:
        chain = chain.upper()
        if chain in WalletServiceFactory.EVM_RPC_URLS:
            rpc_url = WalletServiceFactory.get_rpc_url(chain)
            return EVMWalletService(chain=chain, provider_url=rpc_url)
        else:
            raise NotImplementedError(f"{chain} not supported")
        

# if __name__ == "__main__":
#     # run --> python -m wallet_core.wallets.services.service_factory
#     obj = WalletServiceFactory.get_service("BSC")
#     print(obj.create_wallet())