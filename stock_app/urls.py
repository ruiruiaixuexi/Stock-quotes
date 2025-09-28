from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .test_views import TestView
from .simple_views import (
    SimpleMarketView, SimpleStockListView, SimpleSearchView,
    SimpleStockDetailView, SimpleRealtimeView, SimpleHistoryView
)

urlpatterns = [
    # 简化API端点
    path('market/', SimpleMarketView.as_view(), name='market-overview'),
    path('list/', SimpleStockListView.as_view(), name='stock-list'),
    path('search/', SimpleSearchView.as_view(), name='stock-search'),
    path('stocks/<str:code>/', SimpleStockDetailView.as_view(), name='stock-detail'),
    path('stocks/<str:code>/realtime/', SimpleRealtimeView.as_view(), name='stock-realtime'),
    path('stocks/<str:code>/history/', SimpleHistoryView.as_view(), name='stock-history'),
    
    # 测试端点
    path('test/', TestView.as_view(), name='test'),
]
