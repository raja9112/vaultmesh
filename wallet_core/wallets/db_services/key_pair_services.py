from wallets.models import Wallet, BlockchainNetwork, KeyPair
from wallets.db_services.wallet_services import WalletServices

class KeyPairServices:
    @staticmethod
    def create_record(**payload):
        try:
            keypair_dto = KeyPair(**payload)
            keypair_dto.save()
        except Exception as e:
            return Exception(f"Unable to save the key pair record due to {e}")
        
        return keypair_dto

    @staticmethod
    def get_keypair_by_wallet(wallet_id):
        try:
            return KeyPair.objects.filter(wallet_id=wallet_id).first()
        except Exception as e:
            return Exception(f"Error retrieving key pair by wallet ID: {e}")