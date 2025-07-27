from django.contrib import admin
from .models import Wallet, KeyPair

admin.site.register(Wallet)
admin.site.register(KeyPair)