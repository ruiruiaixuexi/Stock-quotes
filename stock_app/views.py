from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import models
from datetime import datetime, timedelta
import logging

from .models import Stock, StockPrice, StockRealtime
from .serializers import (
    StockSerializer, StockPriceSerializer, StockRealtimeSerializer,
    StockSearchSerializer, MarketOverviewSerializer
)
from .akshare_service import AKShareService

logger = logging.getLogger(__name__)


class StockViewSet(viewsets.ModelViewSet):
    """股票信息视图集"""
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    lookup_field = 'code'
    
    def get_queryset(self):
        queryset = Stock.objects.all()
        market = self.request.query_params.get('market', None)
        if market:
            queryset = queryset.filter(market=market)
        return queryset
    
    @action(detail=True, methods=['get'])
    def realtime(self, request, code=None):
        """获取股票实时行情"""
        try:
            stock = get_object_or_404(Stock, code=code)
            
            # 尝试从数据库获取实时数据
            try:
                realtime_data = stock.realtime
                # 检查数据是否过期（超过5分钟）
                if timezone.now() - realtime_data.updated_at > timedelta(minutes=5):
                    raise StockRealtime.DoesNotExist
                
                serializer = StockRealtimeSerializer(realtime_data)
                return Response(serializer.data)
                
            except StockRealtime.DoesNotExist:
                # 从AKShare获取实时数据
                akshare_service = AKShareService()
                realtime_info = akshare_service.get_stock_realtime(code)
                
                if not realtime_info:
                    return Response(
                        {'error': f'无法获取股票 {code} 的实时数据'},
                        status=status.HTTP_404_NOT_FOUND
                    )
                
                # 更新或创建实时数据
                realtime_data, created = StockRealtime.objects.update_or_create(
                    stock=stock,
                    defaults={
                        'current_price': realtime_info['current_price'],
                        'change_rate': realtime_info['change_rate'],
                        'change_amount': realtime_info['change_amount'],
                        'volume': realtime_info['volume'],
                        'amount': realtime_info['amount'],
                        'high_price': realtime_info['high_price'],
                        'low_price': realtime_info['low_price'],
                        'open_price': realtime_info['open_price'],
                        'pre_close': realtime_info['pre_close'],
                    }
                )
                
                serializer = StockRealtimeSerializer(realtime_data)
                return Response(serializer.data)
                
        except Exception as e:
            logger.error(f"获取股票 {code} 实时数据失败: {str(e)}")
            return Response(
                {'error': '获取实时数据失败'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['get'])
    def history(self, request, code=None):
        """获取股票历史数据"""
        try:
            stock = get_object_or_404(Stock, code=code)
            
            # 获取查询参数
            period = request.query_params.get('period', 'daily')
            start_date = request.query_params.get('start_date')
            end_date = request.query_params.get('end_date')
            
            # 首先尝试从数据库获取
            queryset = stock.prices.all()
            
            if start_date:
                try:
                    start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
                    queryset = queryset.filter(date__gte=start_date_obj)
                except ValueError:
                    pass
            
            if end_date:
                try:
                    end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
                    queryset = queryset.filter(date__lte=end_date_obj)
                except ValueError:
                    pass
            
            # 如果数据库中数据不足，从AKShare获取
            if queryset.count() < 10:
                akshare_service = AKShareService()
                
                # 转换日期格式
                ak_start_date = start_date.replace('-', '') if start_date else None
                ak_end_date = end_date.replace('-', '') if end_date else None
                
                history_data = akshare_service.get_stock_history(
                    code, period, ak_start_date, ak_end_date
                )
                
                # 批量创建历史数据
                price_objects = []
                for data in history_data:
                    price_obj, created = StockPrice.objects.get_or_create(
                        stock=stock,
                        date=data['date'],
                        defaults={
                            'open_price': data['open_price'],
                            'high_price': data['high_price'],
                            'low_price': data['low_price'],
                            'close_price': data['close_price'],
                            'volume': data['volume'],
                            'amount': data['amount'],
                            'change_rate': data['change_rate'],
                        }
                    )
                    if created:
                        price_objects.append(price_obj)
                
                logger.info(f"为股票 {code} 创建了 {len(price_objects)} 条历史数据")
                
                # 重新查询数据库
                queryset = stock.prices.all()
                if start_date:
                    start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
                    queryset = queryset.filter(date__gte=start_date_obj)
                if end_date:
                    end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
                    queryset = queryset.filter(date__lte=end_date_obj)
            
            serializer = StockPriceSerializer(queryset[:100], many=True)  # 限制返回100条
            return Response(serializer.data)
            
        except Exception as e:
            logger.error(f"获取股票 {code} 历史数据失败: {str(e)}")
            return Response(
                {'error': '获取历史数据失败'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class StockSearchView(APIView):
    """股票搜索视图"""
    
    def get(self, request):
        """搜索股票"""
        keyword = request.query_params.get('q', '').strip()
        
        if not keyword:
            return Response(
                {'error': '请提供搜索关键词'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # 首先在数据库中搜索
            db_results = Stock.objects.filter(
                models.Q(code__icontains=keyword) | 
                models.Q(name__icontains=keyword)
            )[:10]
            
            results = []
            
            # 如果数据库中有结果，返回数据库结果
            if db_results.exists():
                for stock in db_results:
                    try:
                        realtime = stock.realtime
                        results.append({
                            'code': stock.code,
                            'name': stock.name,
                            'current_price': float(realtime.current_price),
                            'change_rate': float(realtime.change_rate),
                            'market': stock.market
                        })
                    except StockRealtime.DoesNotExist:
                        results.append({
                            'code': stock.code,
                            'name': stock.name,
                            'current_price': 0.0,
                            'change_rate': 0.0,
                            'market': stock.market
                        })
            else:
                # 从AKShare搜索
                akshare_service = AKShareService()
                search_results = akshare_service.search_stock(keyword)
                
                # 将搜索结果保存到数据库
                for result in search_results:
                    stock, created = Stock.objects.get_or_create(
                        code=result['code'],
                        defaults={
                            'name': result['name'],
                            'market': result['market']
                        }
                    )
                    
                    results.append(result)
            
            serializer = StockSearchSerializer(results, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            logger.error(f"搜索股票失败: {str(e)}")
            return Response(
                {'error': '搜索失败'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class MarketOverviewView(APIView):
    """市场概览视图"""
    
    def get(self, request):
        """获取市场概览数据"""
        try:
            akshare_service = AKShareService()
            overview_data = akshare_service.get_market_overview()
            
            serializer = MarketOverviewSerializer(overview_data)
            return Response(serializer.data)
            
        except Exception as e:
            logger.error(f"获取市场概览失败: {str(e)}")
            return Response(
                {'error': '获取市场概览失败'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class StockListView(APIView):
    """股票列表视图"""
    
    def get(self, request):
        """获取股票列表"""
        try:
            # 检查数据库中是否有股票数据
            if Stock.objects.count() < 10:
                # 从AKShare获取股票列表
                akshare_service = AKShareService()
                stock_list = akshare_service.get_stock_list()
                
                # 批量创建股票记录
                stock_objects = []
                for stock_data in stock_list:
                    stock, created = Stock.objects.get_or_create(
                        code=stock_data['code'],
                        defaults={
                            'name': stock_data['name'],
                            'market': stock_data['market']
                        }
                    )
                    if created:
                        stock_objects.append(stock)
                
                logger.info(f"创建了 {len(stock_objects)} 条股票记录")
            
            # 从数据库返回股票列表
            queryset = Stock.objects.all()
            
            # 支持分页
            page_size = int(request.query_params.get('page_size', 20))
            page = int(request.query_params.get('page', 1))
            
            start = (page - 1) * page_size
            end = start + page_size
            
            stocks = queryset[start:end]
            serializer = StockSerializer(stocks, many=True)
            
            return Response({
                'results': serializer.data,
                'count': queryset.count(),
                'page': page,
                'page_size': page_size
            })
            
        except Exception as e:
            logger.error(f"获取股票列表失败: {str(e)}")
            return Response(
                {'error': '获取股票列表失败'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
