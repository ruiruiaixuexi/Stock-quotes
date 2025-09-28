"""
测试视图 - 用于调试API问题
"""
from django.http import JsonResponse
from django.views import View
import logging

logger = logging.getLogger(__name__)


class TestView(View):
    """测试视图"""
    
    def get(self, request):
        """测试GET请求"""
        try:
            # 测试模拟数据服务
            from .mock_service import MockDataService
            mock_service = MockDataService()
            
            # 获取测试数据
            stocks = mock_service.get_stock_list()
            realtime = mock_service.get_stock_realtime('000001')
            market = mock_service.get_market_overview()
            
            return JsonResponse({
                'status': 'success',
                'message': '测试成功',
                'data': {
                    'stocks_count': len(stocks),
                    'sample_stock': stocks[0] if stocks else None,
                    'realtime_sample': realtime,
                    'market_overview': market
                }
            })
            
        except Exception as e:
            logger.error(f"测试视图错误: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)

