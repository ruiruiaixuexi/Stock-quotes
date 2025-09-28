"""
模拟数据服务 - 用于测试和演示
当AKShare不可用时提供模拟数据
"""
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class MockDataService:
    """模拟数据服务类"""
    
    def __init__(self):
        self.mock_stocks = [
            {'code': '000001', 'name': '平安银行', 'market': 'SZ'},
            {'code': '000002', 'name': '万科A', 'market': 'SZ'},
            {'code': '600000', 'name': '浦发银行', 'market': 'SH'},
            {'code': '600036', 'name': '招商银行', 'market': 'SH'},
            {'code': '000858', 'name': '五粮液', 'market': 'SZ'},
            {'code': '600519', 'name': '贵州茅台', 'market': 'SH'},
            {'code': '000725', 'name': '京东方A', 'market': 'SZ'},
            {'code': '600276', 'name': '恒瑞医药', 'market': 'SH'},
            {'code': '300059', 'name': '东方财富', 'market': 'SZ'},
            {'code': '002415', 'name': '海康威视', 'market': 'SZ'},
        ]
    
    def get_stock_list(self) -> List[Dict]:
        """获取股票列表"""
        logger.info("使用模拟数据获取股票列表")
        return self.mock_stocks
    
    def get_stock_realtime(self, symbol: str) -> Optional[Dict]:
        """获取股票实时行情"""
        # 查找股票
        stock = next((s for s in self.mock_stocks if s['code'] == symbol), None)
        if not stock:
            return None
        
        # 生成模拟实时数据
        base_price = random.uniform(10, 100)
        change_rate = random.uniform(-10, 10)
        change_amount = base_price * change_rate / 100
        
        return {
            'code': symbol,
            'name': stock['name'],
            'current_price': round(base_price, 2),
            'change_rate': round(change_rate, 2),
            'change_amount': round(change_amount, 2),
            'volume': random.randint(1000000, 100000000),
            'amount': random.randint(100000000, 10000000000),
            'high_price': round(base_price * 1.05, 2),
            'low_price': round(base_price * 0.95, 2),
            'open_price': round(base_price * 0.98, 2),
            'pre_close': round(base_price - change_amount, 2),
            'updated_at': datetime.now()
        }
    
    def get_stock_history(self, symbol: str, period: str = "daily", 
                         start_date: str = None, end_date: str = None) -> List[Dict]:
        """获取股票历史数据"""
        # 生成30天的模拟历史数据
        history_data = []
        base_price = random.uniform(10, 100)
        
        for i in range(30):
            date = datetime.now() - timedelta(days=i)
            
            # 模拟价格波动
            daily_change = random.uniform(-0.05, 0.05)
            open_price = base_price * (1 + daily_change)
            high_price = open_price * random.uniform(1.0, 1.05)
            low_price = open_price * random.uniform(0.95, 1.0)
            close_price = open_price * random.uniform(0.98, 1.02)
            
            change_rate = (close_price - base_price) / base_price * 100
            
            history_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'open_price': round(open_price, 2),
                'high_price': round(high_price, 2),
                'low_price': round(low_price, 2),
                'close_price': round(close_price, 2),
                'volume': random.randint(1000000, 50000000),
                'amount': random.randint(100000000, 5000000000),
                'change_rate': round(change_rate, 2)
            })
            
            base_price = close_price  # 下一天的基准价格
        
        return sorted(history_data, key=lambda x: x['date'])
    
    def search_stock(self, keyword: str) -> List[Dict]:
        """搜索股票"""
        keyword = keyword.upper()
        results = []
        
        for stock in self.mock_stocks:
            if keyword in stock['code'] or keyword in stock['name']:
                realtime = self.get_stock_realtime(stock['code'])
                results.append({
                    'code': stock['code'],
                    'name': stock['name'],
                    'current_price': realtime['current_price'],
                    'change_rate': realtime['change_rate'],
                    'market': stock['market']
                })
        
        return results
    
    def get_market_overview(self) -> Dict:
        """获取市场概览数据"""
        return {
            'sh_index': {
                'name': '上证指数',
                'current': round(random.uniform(3000, 3500), 2),
                'change_rate': round(random.uniform(-2, 2), 2),
                'change_amount': round(random.uniform(-50, 50), 2)
            },
            'sz_index': {
                'name': '深证成指',
                'current': round(random.uniform(10000, 12000), 2),
                'change_rate': round(random.uniform(-2, 2), 2),
                'change_amount': round(random.uniform(-200, 200), 2)
            },
            'total_stocks': len(self.mock_stocks),
            'up_count': random.randint(3, 7),
            'down_count': random.randint(2, 5),
            'flat_count': random.randint(0, 2)
        }

