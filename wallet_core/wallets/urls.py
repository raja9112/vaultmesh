from django.urls import path, include
from wallets.views.auth import CustomTokenVerifyView


urlpatterns = [
    path('auth/jwt/verify/', CustomTokenVerifyView.as_view(), name='jwt-verify'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
