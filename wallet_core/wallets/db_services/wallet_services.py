from wallets.models import Wallet
from django.db import transaction


class WalletServices():

    @staticmethod
    def create_record(**payload):
        try:
            model_fields = {f.name for f in Wallet._meta.get_fields()}
            clean_payload = {k: v for k, v in payload.items() if k in model_fields}
            with transaction.atomic():
                wallet_dto = Wallet(**clean_payload)
                wallet_dto.save()
                return wallet_dto
        except Exception as e:
            raise e
        
    @staticmethod
    def get_wallet_dto_by_address(wallet_address):
        try:
            return Wallet.objects.get(wallet_address=wallet_address)
        except Wallet.DoesNotExist:
            return None
        except Exception as e:
            return Exception(f"Error retrieving wallet by address: {e}")