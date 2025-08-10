import jwt
import datetime
from django.conf import settings
from django.http import JsonResponse
from wallets.views.enums import JwtErrorCode
from wallets.views.exceptions import GenericApiException, ExternalApiResponseWrapper
from rest_framework.response import Response

def create_jwt(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=1)
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token


def jwt_required(view_func):
    def wrapper(request, *args, **kwargs):
        token = request.headers.get("X-Authorization")
        if not token:
            return JsonResponse(GenericApiException(success=False, code=JwtErrorCode.INVALID_TOKEN.value, data={"error": "Missing or Invalid token"}).__dict__, safe=False)
        try:
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            request.user_id = decoded["user_id"]
        except jwt.ExpiredSignatureError:
            return JsonResponse(GenericApiException(success=False, code=JwtErrorCode.TOKEN_EXPIRED.value, data={"error": "Token has expired"}).__dict__, safe=False)
        except jwt.InvalidTokenError:
            return JsonResponse(GenericApiException(success=False, code=JwtErrorCode.INVALID_TOKEN.value, data={"error": "Invalid token"}).__dict__, safe=False)
        return view_func(request, *args, **kwargs)
    return wrapper
