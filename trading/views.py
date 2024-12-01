from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Trade, ClosedTrade
from .DexScreener import DexScanner
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse


def hello_sniper(request):
    return HttpResponse("Hello Sniper")


@csrf_exempt
def open_trade(request):
    if request.method == "POST":
        data = json.loads(request.body)
        token_address = data.get("token_address")

        if not token_address:
            return JsonResponse({"error": "Token address is required"}, status=400)

        dex_screener = DexScanner()
        token_data = dex_screener.fetchTokensData([token_address])

        print(token_data)

        # Create and save the trade
        trade = Trade(
            token_address=token_address,
            name=token_data["name"],
            symbol=token_data["symbol"],
            market_cap=token_data["marketCap"],
            image_url=token_data["imageUrl"],
            price_usd=token_data["priceUsd"],
        )
        trade.save()

        return JsonResponse(
            {"trade_id": str(trade.trade_id), "message": "Trade opened successfully"}
        )

    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def get_trade(request):
    if request.method == "POST":
        data = json.loads(request.body)
        trade_id = data.get("trade_id")

        if not trade_id:
            return JsonResponse({"error": "Trade ID is required"}, status=400)

        trade = get_object_or_404(Trade, trade_id=trade_id)

        trade_data = {
            "trade_id": str(trade.trade_id),
            "token_address": trade.token_address,
            "name": trade.name,
            "symbol": trade.symbol,
            "market_cap": trade.market_cap,
            "image_url": trade.image_url,
            "price_usd": trade.price_usd,
            "created_at": trade.created_at,
        }

        return JsonResponse(trade_data)

    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def get_open_trades(request):
    if request.method == "GET":
        trades = Trade.objects.all()
        trades_data = []

        for trade in trades:
            trade_data = {
                "trade_id": str(trade.trade_id),
                "token_address": trade.token_address,
                "name": trade.name,
                "symbol": trade.symbol,
                "market_cap": trade.market_cap,
                "image_url": trade.image_url,
                "price_usd": trade.price_usd,
                "created_at": trade.created_at,
            }
            trades_data.append(trade_data)

        return JsonResponse(trades_data, safe=False)

    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def close_trade(request):
    if request.method == "POST":
        data = json.loads(request.body)
        trade_id = data.get("trade_id")

        if not trade_id:
            return JsonResponse({"error": "Trade ID is required"}, status=400)

        trade = get_object_or_404(Trade, trade_id=trade_id)

        dex_screener = DexScanner()
        token_data = dex_screener.fetchTokensData([trade.token_address])
        current_price_usd = float(token_data["priceUsd"])  # Convert to float

        # Calculate PnL in percentage
        pnl_percentage = round(
            ((current_price_usd - trade.price_usd) / trade.price_usd) * 100, 2
        )

        # Create and save the closed trade
        closed_trade = ClosedTrade(
            trade_id=trade.trade_id,
            token_address=trade.token_address,
            name=trade.name,
            symbol=trade.symbol,
            market_cap=trade.market_cap,
            image_url=trade.image_url,
            price_usd=trade.price_usd,
            created_at=trade.created_at,
            pnl_percentage=pnl_percentage,
        )
        closed_trade.save()

        # Delete the open trade
        trade.delete()

        return JsonResponse(
            {
                "trade_id": str(closed_trade.trade_id),
                "pnl_percentage": pnl_percentage,
                "message": "Trade closed successfully",
            }
        )

    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def get_closed_trades(request):
    if request.method == "GET":
        closed_trades = ClosedTrade.objects.all()
        closed_trades_data = []

        for trade in closed_trades:
            trade_data = {
                "trade_id": str(trade.trade_id),
                "token_address": trade.token_address,
                "name": trade.name,
                "symbol": trade.symbol,
                "market_cap": trade.market_cap,
                "image_url": trade.image_url,
                "price_usd": trade.price_usd,
                "created_at": trade.created_at,
                "closed_at": trade.closed_at,
                "pnl_percentage": trade.pnl_percentage,
            }
            closed_trades_data.append(trade_data)

        return JsonResponse(closed_trades_data, safe=False)

    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def get_current_pnl(request):
    if request.method == "POST":
        data = json.loads(request.body)
        trade_id = data.get("trade_id")

        if not trade_id:
            return JsonResponse({"error": "Trade ID is required"}, status=400)

        trade = get_object_or_404(Trade, trade_id=trade_id)

        dex_screener = DexScanner()
        token_data = dex_screener.fetchTokensData([trade.token_address])
        current_price_usd = float(token_data["priceUsd"])  # Convert to float

        # Calculate current PnL in percentage
        pnl_percentage = round(
            ((current_price_usd - trade.price_usd) / trade.price_usd) * 100, 2
        )

        return JsonResponse(
            {
                "trade_id": str(trade.trade_id),
                "current_price_usd": current_price_usd,
                "pnl_percentage": pnl_percentage,
            }
        )

    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def clear_closed_trades(request):
    if request.method == "POST":
        ClosedTrade.objects.all().delete()
        return JsonResponse({"message": "All closed trades have been cleared"})

    return JsonResponse({"error": "Invalid request method"}, status=405)
