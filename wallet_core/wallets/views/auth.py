from rest_framework_simplejwt.serializers import TokenVerifySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class CustomTokenVerifyView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = TokenVerifySerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            return Response({"success": True, "detail": "Token is valid"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"success": False, "detail": "Token is not valid"}, status=status.HTTP_401_UNAUTHORIZED)
