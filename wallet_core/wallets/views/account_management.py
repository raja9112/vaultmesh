from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from wallets.services.service_factory import WalletServiceFactory
from wallets.views.utils import jwt_required
from wallets.views.exceptions import GenericApiException, ExternalApiResponseWrapper
from wallets.views.enums import StatusCode

@csrf_exempt
# @jwt_required
@api_view(['POST'])
def create_wallet_address(request):
    chain = request.data.get('chain', '').upper()
    if not chain:
        raise GenericApiException(success=False, code=StatusCode.MISSING_INPUT.value, data={"chain": chain})
    try:
        chain_dto = WalletServiceFactory.get_service(chain)
        wallet_data = chain_dto.create_wallet()
        response = {
            "address": wallet_data.get("address"),
            "private_key": wallet_data.get("private_key_hex"),
            "chain": chain,
        }
        response_wrapper = ExternalApiResponseWrapper(success=True, code=StatusCode.SUCCESS.value, data=response)
        return Response(response_wrapper.__dict__)
    except NotImplementedError as e:
        return GenericApiException(success=False, code=StatusCode.NOT_IMPLEMENTED.value, data={"error": str(e)})

