from django.db import models
from django.contrib.auth.models import User


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta: 
        abstract = True


class Wallet(TimeStampMixin):
    WALLET_TYPE_CHOICES = [
        ('custodial', 'Custodial'),
        ('non_custodial', 'Non-Custodial'),
    ]
    STORAGE_TYPE_CHOICES = [
        ("hot", 'Hot'),
        ("cold", 'Cold'),
    ]
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wallet_address = models.CharField(max_length=255, unique=True)
    wallet_type = models.CharField(max_length=20, choices=WALLET_TYPE_CHOICES, default='custodial')
    storage_type = models.CharField(max_length=20, choices=STORAGE_TYPE_CHOICES, default='hot')
    chain_symbol = models.CharField(max_length=20, null=True)
    network_type = models.CharField(max_length=20, null=True)
    wallet_format = models.CharField(max_length=50, null=True)
    address_index = models.CharField(max_length=512, null=True)

    class Meta:
        db_table = 'wallet'
        indexes = [
            models.Index(fields=['id', 'wallet_address'])
        ]


class KeyPair(TimeStampMixin):
    id = models.AutoField(primary_key=True)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    public_key = models.TextField()
    private_key = models.TextField(null=True)
    key_format = models.CharField(max_length=20, default="base64")
    encryption_iv = models.CharField(max_length=255, null=True)
    encryption_algorithm = models.CharField(max_length=20, default="AES-256")
    is_active = models.BooleanField(default=True)
    derivation_path = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'key_pair'
        constraints = [
            models.UniqueConstraint(fields=['wallet', 'public_key', 'private_key'], name='unique-wallet-keys')
        ]
        indexes = [
            models.Index(fields=['id', 'wallet'])
        ]