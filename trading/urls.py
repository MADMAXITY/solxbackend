from django.urls import path
from . import views

urlpatterns = [
    path("open-trade/", views.open_trade, name="open_trade"),
    path("get-trade/", views.get_trade, name="get_trade"),
    path("get-open-trades/", views.get_open_trades, name="get_open_trades"),
    path("close-trade/", views.close_trade, name="close_trade"),
    path("get-closed-trades/", views.get_closed_trades, name="get_closed_trades"),
    path("get-current-pnl/", views.get_current_pnl, name="get_current_pnl"),
    path("clear-closed-trades/", views.clear_closed_trades, name="clear_closed_trades"),
    path("", views.hello_sniper, name="hello_sniper"),
]
