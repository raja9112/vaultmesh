from wallets.models import Wallet, BlockchainNetwork

class BlockchainNetworkServices:
    
    @staticmethod
    def create_record(**payload):
        try:
            network_dto = BlockchainNetwork(**payload)
            network_dto.save()
        except Exception as e:
            return Exception(f"Unable to save the blockchain network record due to {e}")
        
        return network_dto

    @staticmethod
    def get_chain_detail_by_symbol(chain_symbol, network_type=None):
        try:
            return BlockchainNetwork.objects.get(chain_symbol=chain_symbol, network_type=network_type)
        except BlockchainNetwork.DoesNotExist:
            return None