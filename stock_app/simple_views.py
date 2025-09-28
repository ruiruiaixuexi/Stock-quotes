"""
简化视图 - 避免复杂依赖问题
"""
from django.http import JsonResponse
from django.views import View
from .mock_service import MockDataService
import logging

logger = logging.getLogger(__name__)


class SimpleMarketView(View):
    """简化市场概览视图"""
    
    def get(self, request):
        try:
            mock_service = MockDataService()
            data = mock_service.get_market_overview()
            return JsonResponse(data)
        except Exception as e:
            logger.error(f"市场概览错误: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)


class SimpleStockListView(View):
    """简化股票列表视图"""
    
    def get(self, request):
        try:
            mock_service = MockDataService()
            stocks = mock_service.get_stock_list()
            
            # 添加实时价格
            for stock in stocks:
                realtime = mock_service.get_stock_realtime(stock['code'])
                if realtime:
                    stock.update({
                        'current_price': realtime['current_price'],
                        'change_rate': realtime['change_rate']
                    })
            
            return JsonResponse({
                'results': stocks,
                'count': len(stocks),
                'page': 1,
                'page_size': len(stocks)
            })
        except Exception as e:
            logger.error(f"股票列表错误: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)


class SimpleSearchView(View):
    """简化搜索视图"""
    
    def get(self, request):
        try:
            keyword = request.GET.get('q', '').strip()
            if not keyword:
                return JsonResponse({'error': '请提供搜索关键词'}, status=400)
            
            mock_service = MockDataService()
            results = mock_service.search_stock(keyword)
            
            return JsonResponse(results, safe=False)
        except Exception as e:
            logger.error(f"搜索错误: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)


class SimpleStockDetailView(View):
    """简化股票详情视图"""
    
    def get(self, request, code):
        try:
            mock_service = MockDataService()
            
            # 查找股票
            stocks = mock_service.get_stock_list()
            stock = next((s for s in stocks if s['code'] == code), None)
            
            if not stock:
                return JsonResponse({'error': '股票不存在'}, status=404)
            
            return JsonResponse(stock)
        except Exception as e:
            logger.error(f"股票详情错误: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)


class SimpleRealtimeView(View):
    """简化实时行情视图"""
    
    def get(self, request, code):
        try:
            mock_service = MockDataService()
            realtime = mock_service.get_stock_realtime(code)
            
            if not realtime:
                return JsonResponse({'error': '无法获取实时数据'}, status=404)
            
            return JsonResponse(realtime)
        except Exception as e:
            logger.error(f"实时行情错误: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)


class SimpleHistoryView(View):
    """简化历史数据视图"""
    
    def get(self, request, code):
        try:
            mock_service = MockDataService()
            history = mock_service.get_stock_history(code)
            
            return JsonResponse(history, safe=False)
        except Exception as e:
            logger.error(f"历史数据错误: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)

