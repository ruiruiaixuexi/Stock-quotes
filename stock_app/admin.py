from django.contrib import admin
from .models import Stock, StockPrice, StockRealtime


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'market', 'industry', 'created_at']
    list_filter = ['market', 'industry', 'created_at']
    search_fields = ['code', 'name']
    ordering = ['code']


@admin.register(StockPrice)
class StockPriceAdmin(admin.ModelAdmin):
    list_display = ['stock', 'date', 'open_price', 'high_price', 'low_price', 'close_price', 'volume', 'change_rate']
    list_filter = ['date', 'stock__market']
    search_fields = ['stock__code', 'stock__name']
    ordering = ['-date']
    date_hierarchy = 'date'


@admin.register(StockRealtime)
class StockRealtimeAdmin(admin.ModelAdmin):
    list_display = ['stock', 'current_price', 'change_rate', 'change_amount', 'volume', 'updated_at']
    list_filter = ['updated_at', 'stock__market']
    search_fields = ['stock__code', 'stock__name']
    ordering = ['-updated_at']
    readonly_fields = ['updated_at']
