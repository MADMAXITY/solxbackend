from django.db import models
import uuid


class Trade(models.Model):
    trade_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    token_address = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    market_cap = models.FloatField()
    image_url = models.URLField()
    price_usd = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)


class ClosedTrade(models.Model):
    trade_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    token_address = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    market_cap = models.FloatField()
    image_url = models.URLField()
    price_usd = models.FloatField()
    created_at = models.DateTimeField()
    closed_at = models.DateTimeField(auto_now_add=True)
    pnl_percentage = models.FloatField()
