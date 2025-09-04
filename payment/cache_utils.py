from django.core.cache import cache
import json
from django.db import transaction

def get_cached_wallet(username):
    cache_key = f"user_{username}_wallet"
    data = cache.get(cache_key)
    if not data:
        from .models import Wallet  # Import here to avoid circular imports
        wallet = Wallet.objects.get(user=username)
        data = {
            'balance': float(wallet.balance),
            'stock_equity': float(wallet.stock_eq)
        }
        cache.set(cache_key, json.dumps(data))
    else:
        data = json.loads(data)
    return data


def get_cached_stocks(username):
    cache_key = f"user_{username}_stocks"
    data = cache.get(cache_key)
    if not data:
        from .models import Stock_Wallet  # Import here to avoid circular imports
        wallet = Stock_Wallet.objects.get(user=username)
        data = {
            'balance': float(wallet.balance),
            'stock_equity': float(wallet.stock_eq)
        }
        cache.set(cache_key, json.dumps(data))
    else:
        data = json.loads(data)
    return data


def invalidate_wallet_cache(username):
    cache.delete(f"user_{username}_wallet")