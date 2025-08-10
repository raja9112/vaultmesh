from wallets.db_services.wallet_services import WalletServices
from wallets.db_services.key_pair_services import KeyPairServices
from wallets.db_services.blockchain_network import BlockchainNetworkServices
from wallets.services.service_factory import WalletServiceFactory
from wallets.views.exceptions import GenericApiException, ExternalApiResponseWrapper
from wallets.views.enums import StatusCode, WalletType
from wallets.views.cipher_management import CipherUtility
from django.http import JsonResponse
from decouple import config
from django.contrib.auth import get_user_model



def handle_custodial_wallet(chain):
    chain_service = WalletServiceFactory.get_service(chain)
    if isinstance(chain_service, dict) and chain_service.get("success") is False:
        return chain_service
    wallet_data = chain_service.create_wallet()
    response = {
        "address": wallet_data.get("address"),
        "chain": chain,
    }
    return response, wallet_data


def handle_non_custodial_wallet(chain):
    chain_service = WalletServiceFactory.get_service(chain)
    if isinstance(chain_service, dict) and chain_service.get("success") is False:
        return chain_service
    wallet_data = chain_service.create_wallet()
    response = {
        "address": wallet_data.get("address"),
        "private_key": wallet_data.get("private_key_hex"),
        "chain": chain,
    }
    return response, wallet_data


def generate_payload(request, wallet_data):
    print("Hello")
    network_type = _get_network_type()
    blockchain_network = _get_blockchain_network(request, network_type)
    if not blockchain_network:
        return _error_response(StatusCode.BAD_REQUEST, "Invalid chain symbol specified")
    print("world")

    wallet_payload = _build_wallet_payload(request, wallet_data, blockchain_network)
    WalletServices.create_record(**wallet_payload)
    print("Vanakam")

    wallet_dto = _get_wallet_dto(wallet_data)
    if not wallet_dto:
        return _error_response(StatusCode.NOT_FOUND, "Wallet with this address already exists")
    print("collie")

    keypair_payload = _build_keypair_payload(request, wallet_data, wallet_dto)
    KeyPairServices.create_record(**keypair_payload)



def _get_network_type():
    return "mainnet" if config("NETWORK_TYPE") == "MAINNET" else "testnet"


def _get_blockchain_network(request, network_type):
    chain_symbol = request.data.get('chain', '').upper()
    return BlockchainNetworkServices.get_chain_detail_by_symbol(chain_symbol, network_type=network_type)


def _error_response(status_code, message):
    return JsonResponse(
        GenericApiException(
            success=False,
            code=status_code.value,
            data={"error": message}
        ).__dict__,
        safe=False
    )


def _build_wallet_payload(request, wallet_data, blockchain_network):
    User = get_user_model()
    user_obj = User.objects.get(id=request.user_id)
    return {
        "user": user_obj,
        "wallet_name": request.data.get('wallet_name', ''),
        "wallet_address": wallet_data.get("address"),
        "wallet_type": request.data.get('wallet_type', '').lower(),
        "storage_type": request.data.get('storage_type', '').lower(),
        "chain": blockchain_network,
        "wallet_format": wallet_data.get("wallet_format", ""),
        "address_index": request.data.get('address_index', ''),
    }


def _get_wallet_dto(wallet_data):
    return WalletServices.get_wallet_dto_by_address(wallet_data.get("address"))


def _build_keypair_payload(request, wallet_data, wallet_dto):
    encrypted_private_key = {}
    if request.data.get('wallet_type', '').lower() == WalletType.CUSTODIAL.value:
        cipher = CipherUtility()
        encrypted_private_key = cipher.encrypt_private_key(wallet_data.get("private_key_bytes", b""))

    return {
        "wallet": wallet_dto,
        "public_key": wallet_data.get("public_key_hex", ""),
        "private_key": encrypted_private_key.get("ciphertext", ""),
        "additional_data": {
            "iv": encrypted_private_key.get("iv", ""),
            "salt": encrypted_private_key.get("salt", ""),
        }
    }
