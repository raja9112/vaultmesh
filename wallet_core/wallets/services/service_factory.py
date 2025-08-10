from .evm_chain_service import EVMWalletService
from decouple import config
from django.http import JsonResponse


class WalletServiceFactory:
    EVM_RPC_URLS = {
        "ETH": config("ETHEREUM_TESTNET"),     # For testnet
        "BSC": config("BSC_TESTNET"),
        "POLYGON": config("POLYGON_TESTNET"),
        "AVALANCHE": config("AVALANCHE_TESTNET"),
    }

    @staticmethod
    def get_rpc_url(chain):
        try:
            return WalletServiceFactory.EVM_RPC_URLS[chain.upper()]
        except KeyError:
            raise NotImplementedError(f"RPC URL for {chain} not configured")

    @staticmethod
    def get_service(chain: str):
        chain = chain.upper()
        if chain in WalletServiceFactory.EVM_RPC_URLS:
            rpc_url = WalletServiceFactory.get_rpc_url(chain)
            return EVMWalletService(chain=chain, provider_url=rpc_url)
        else:
            return {"success": False, "error": f"Service for {chain} not implemented"}
        

# if __name__ == "__main__":
#     # run --> python -m wallet_core.wallets.services.service_factory
#     obj = WalletServiceFactory.get_service("BSC")
#     print(obj.create_wallet())