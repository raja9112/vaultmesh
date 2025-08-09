from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from wallets.views.enums import StatusCode
from wallets.views.utils import create_jwt
from wallets.views.exceptions import GenericApiException, ExternalApiResponseWrapper


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            username = request.data.get("username", "")
            password = request.data.get("password", "")
            if not username or not password:
                raise GenericApiException(
                    success=False,
                    code=StatusCode.MISSING_CREDENTIALS.value,
                    data={"username": username, "password": password}
                )
            user = authenticate(username=username, password=password)
            if user is None:
                raise GenericApiException(
                    success=False,
                    code=StatusCode.USER_NOT_REGISTERED.value,
                    data={"username": username, "password": password}
                )
            token = create_jwt(user.id)
            response_wrapper = ExternalApiResponseWrapper(
                success=True,
                code=StatusCode.SUCCESS.value,
                data={"token": token}
            )
            return Response(response_wrapper.__dict__)
        except GenericApiException as exc:
            return Response(exc.__dict__)
