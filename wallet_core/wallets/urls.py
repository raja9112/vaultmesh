from django.urls import path, include
from wallets.views.auth import LoginView
from wallets.views.account_management import create_wallet_address


urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

    path('wallets/create/', create_wallet_address, name='create_wallet_address'),
]
