from rest_framework import serializers
from .models import Stock, StockPrice, StockRealtime


class StockSerializer(serializers.ModelSerializer):
    """股票基本信息序列化器"""
    
    class Meta:
        model = Stock
        fields = ['id', 'code', 'name', 'market', 'industry', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class StockPriceSerializer(serializers.ModelSerializer):
    """股票价格数据序列化器"""
    stock_code = serializers.CharField(source='stock.code', read_only=True)
    stock_name = serializers.CharField(source='stock.name', read_only=True)
    change_amount = serializers.ReadOnlyField()
    
    class Meta:
        model = StockPrice
        fields = [
            'id', 'stock_code', 'stock_name', 'date', 
            'open_price', 'high_price', 'low_price', 'close_price',
            'volume', 'amount', 'change_rate', 'change_amount', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class StockRealtimeSerializer(serializers.ModelSerializer):
    """实时股票数据序列化器"""
    stock_code = serializers.CharField(source='stock.code', read_only=True)
    stock_name = serializers.CharField(source='stock.name', read_only=True)
    
    class Meta:
        model = StockRealtime
        fields = [
            'stock_code', 'stock_name', 'current_price', 'change_rate', 
            'change_amount', 'volume', 'amount', 'high_price', 'low_price',
            'open_price', 'pre_close', 'updated_at'
        ]
        read_only_fields = ['updated_at']


class StockSearchSerializer(serializers.Serializer):
    """股票搜索结果序列化器"""
    code = serializers.CharField()
    name = serializers.CharField()
    current_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    change_rate = serializers.DecimalField(max_digits=6, decimal_places=2)
    market = serializers.CharField()


class MarketOverviewSerializer(serializers.Serializer):
    """市场概览序列化器"""
    sh_index = serializers.DictField(allow_null=True)
    sz_index = serializers.DictField(allow_null=True)
    total_stocks = serializers.IntegerField()
    up_count = serializers.IntegerField()
    down_count = serializers.IntegerField()
    flat_count = serializers.IntegerField()
