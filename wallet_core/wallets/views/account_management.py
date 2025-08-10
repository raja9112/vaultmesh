from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from wallets.views.utils import jwt_required
from wallets.views.exceptions import GenericApiException, ExternalApiResponseWrapper
from wallets.views.enums import StatusCode, WalletType, StorageType
from wallets.views.account_management_helper import handle_custodial_wallet, handle_non_custodial_wallet, generate_payload

@csrf_exempt
@jwt_required
@api_view(['POST'])
def create_wallet_address(request):
    wallet_name = request.data.get('wallet_name', '')
    wallet_type = request.data.get('wallet_type', '').lower()
    storage_type = request.data.get('storage_type', '').lower()
    chain = request.data.get('chain', '').upper()
    if not chain or not wallet_name or not wallet_type or not storage_type:
        return JsonResponse(GenericApiException(success=False, code=StatusCode.MISSING_INPUT.value, data={"error": "Missing required input parameters"}).__dict__, safe=False)
    
    is_valid_storage_type = storage_type in [StorageType.HOT.value, StorageType.COLD.value]
    if not is_valid_storage_type:
        return JsonResponse(GenericApiException(success=False, code=StatusCode.BAD_REQUEST.value, data={"error": "Invalid storage type specified"}).__dict__, safe=False)
    try:
        if wallet_type == WalletType.CUSTODIAL.value:
            response, wallet_data = handle_custodial_wallet(chain)
            generate_payload(request, wallet_data)
        elif wallet_type == WalletType.NON_CUSTODIAL.value:
            response, wallet_data = handle_non_custodial_wallet(chain)
            generate_payload(request, wallet_data)
        else:
            return JsonResponse(GenericApiException(success=False, code=StatusCode.BAD_REQUEST.value, data={"error": "Invalid wallet type specified"}).__dict__, safe=False)
    except Exception as e:
        return JsonResponse(GenericApiException(success=False, code=StatusCode.INTERNAL_SERVER_ERROR.value, data={f"error: Unable to reach server or create wallet due to {e}, Please try again after some time."}).__dict__, safe=False)
        
    response_wrapper = ExternalApiResponseWrapper(success=True, code=StatusCode.SUCCESS.value, data=response)
    return JsonResponse(response_wrapper.__dict__, safe=False)
