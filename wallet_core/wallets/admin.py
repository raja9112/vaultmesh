from django.contrib import admin
from .models import Wallet, KeyPair, BlockchainNetwork

admin.site.register(Wallet)
admin.site.register(BlockchainNetwork)
admin.site.register(KeyPair)