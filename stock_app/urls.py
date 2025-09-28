from django.urls import path
from .simple_views import (
    SimpleMarketView, SimpleStockListView, SimpleSearchView,
    SimpleStockDetailView, SimpleRealtimeView, SimpleHistoryView
)

urlpatterns = [
    # API端点
    path('market/', SimpleMarketView.as_view(), name='market-overview'),
    path('list/', SimpleStockListView.as_view(), name='stock-list'),
    path('search/', SimpleSearchView.as_view(), name='stock-search'),
    path('stocks/<str:code>/', SimpleStockDetailView.as_view(), name='stock-detail'),
    path('stocks/<str:code>/realtime/', SimpleRealtimeView.as_view(), name='stock-realtime'),
    path('stocks/<str:code>/history/', SimpleHistoryView.as_view(), name='stock-history'),
]
