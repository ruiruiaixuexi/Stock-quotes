"""
AKShare数据获取服务
提供股票数据的获取和处理功能
"""
try:
    import akshare as ak
    AKSHARE_AVAILABLE = True
except ImportError:
    AKSHARE_AVAILABLE = False
    ak = None

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    pd = None
from datetime import datetime, timedelta
from django.conf import settings
import logging
from typing import Dict, List, Optional, Union
import time

logger = logging.getLogger(__name__)

# 如果AKShare不可用，导入模拟服务
if not AKSHARE_AVAILABLE:
    from .mock_service import MockDataService
    logger.warning("AKShare不可用，将使用模拟数据服务")


class AKShareService:
    """AKShare数据服务类"""
    
    def __init__(self):
        self.timeout = getattr(settings, 'AKSHARE_TIMEOUT', 30)
        self.retry_count = getattr(settings, 'AKSHARE_RETRY_COUNT', 3)
        
        # 如果AKShare不可用，使用模拟服务
        if not AKSHARE_AVAILABLE:
            self.mock_service = MockDataService()
            logger.info("初始化模拟数据服务")
    
    def _retry_request(self, func, *args, **kwargs):
        """重试机制装饰器"""
        for attempt in range(self.retry_count):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.warning(f"第{attempt + 1}次请求失败: {str(e)}")
                if attempt == self.retry_count - 1:
                    raise e
                time.sleep(1)  # 等待1秒后重试
    
    def get_stock_list(self) -> List[Dict]:
        """
        获取股票列表
        返回: [{'code': '000001', 'name': '平安银行', 'market': 'SZ'}, ...]
        """
        if not AKSHARE_AVAILABLE:
            return self.mock_service.get_stock_list()
            
        try:
            # 获取沪深A股股票列表
            df_sh = self._retry_request(ak.stock_info_sh_name_code, symbol="主板A股")
            df_sz = self._retry_request(ak.stock_zh_a_spot_em)
            
            stocks = []
            
            # 处理上海股票
            if df_sh is not None and not df_sh.empty:
                for _, row in df_sh.iterrows():
                    stocks.append({
                        'code': row['SECURITY_CODE_A'],
                        'name': row['SECURITY_ABBR_A'],
                        'market': 'SH'
                    })
            
            # 处理深圳股票（从实时数据中提取）
            if df_sz is not None and not df_sz.empty:
                sz_stocks = df_sz[df_sz['代码'].str.startswith(('000', '002', '300'))]
                for _, row in sz_stocks.iterrows():
                    stocks.append({
                        'code': row['代码'],
                        'name': row['名称'],
                        'market': 'SZ'
                    })
            
            logger.info(f"成功获取{len(stocks)}只股票信息")
            return stocks[:100]  # 限制返回数量，避免过多数据
            
        except Exception as e:
            logger.error(f"获取股票列表失败: {str(e)}")
            return []
    
    def get_stock_realtime(self, symbol: str) -> Optional[Dict]:
        """
        获取股票实时行情
        参数: symbol - 股票代码，如 '000001'
        返回: 实时行情数据字典
        """
        if not AKSHARE_AVAILABLE:
            return self.mock_service.get_stock_realtime(symbol)
            
        try:
            # 获取实时行情数据
            df = self._retry_request(ak.stock_zh_a_spot_em)
            
            if df is None or df.empty:
                return None
            
            # 查找指定股票
            stock_data = df[df['代码'] == symbol]
            
            if stock_data.empty:
                logger.warning(f"未找到股票 {symbol} 的实时数据")
                return None
            
            row = stock_data.iloc[0]
            
            return {
                'code': row['代码'],
                'name': row['名称'],
                'current_price': float(row['最新价']),
                'change_rate': float(row['涨跌幅']),
                'change_amount': float(row['涨跌额']),
                'volume': int(row['成交量']),
                'amount': float(row['成交额']),
                'high_price': float(row['最高']),
                'low_price': float(row['最低']),
                'open_price': float(row['今开']),
                'pre_close': float(row['昨收']),
                'updated_at': datetime.now()
            }
            
        except Exception as e:
            logger.error(f"获取股票 {symbol} 实时行情失败: {str(e)}")
            return None
    
    def get_stock_history(self, symbol: str, period: str = "daily", 
                         start_date: str = None, end_date: str = None) -> List[Dict]:
        """
        获取股票历史数据
        参数:
            symbol: 股票代码
            period: 周期 ('daily', 'weekly', 'monthly')
            start_date: 开始日期 'YYYYMMDD'
            end_date: 结束日期 'YYYYMMDD'
        返回: 历史数据列表
        """
        if not AKSHARE_AVAILABLE:
            return self.mock_service.get_stock_history(symbol, period, start_date, end_date)
            
        try:
            # 设置默认日期范围（最近30天）
            if not end_date:
                end_date = datetime.now().strftime('%Y%m%d')
            if not start_date:
                start_date = (datetime.now() - timedelta(days=30)).strftime('%Y%m%d')
            
            # 获取历史数据
            df = self._retry_request(
                ak.stock_zh_a_hist,
                symbol=symbol,
                period=period,
                start_date=start_date,
                end_date=end_date,
                adjust=""
            )
            
            if df is None or df.empty:
                return []
            
            history_data = []
            for _, row in df.iterrows():
                history_data.append({
                    'date': row['日期'],
                    'open_price': float(row['开盘']),
                    'high_price': float(row['最高']),
                    'low_price': float(row['最低']),
                    'close_price': float(row['收盘']),
                    'volume': int(row['成交量']),
                    'amount': float(row['成交额']),
                    'change_rate': float(row['涨跌幅']) if '涨跌幅' in row else 0
                })
            
            logger.info(f"成功获取股票 {symbol} 历史数据 {len(history_data)} 条")
            return history_data
            
        except Exception as e:
            logger.error(f"获取股票 {symbol} 历史数据失败: {str(e)}")
            return []
    
    def search_stock(self, keyword: str) -> List[Dict]:
        """
        搜索股票
        参数: keyword - 搜索关键词（股票代码或名称）
        返回: 匹配的股票列表
        """
        if not AKSHARE_AVAILABLE:
            return self.mock_service.search_stock(keyword)
            
        try:
            # 获取实时数据进行搜索
            df = self._retry_request(ak.stock_zh_a_spot_em)
            
            if df is None or df.empty:
                return []
            
            # 按代码或名称搜索
            keyword = keyword.upper()
            matched_stocks = df[
                (df['代码'].str.contains(keyword, na=False)) |
                (df['名称'].str.contains(keyword, na=False))
            ]
            
            results = []
            for _, row in matched_stocks.head(20).iterrows():  # 限制返回20条
                results.append({
                    'code': row['代码'],
                    'name': row['名称'],
                    'current_price': float(row['最新价']),
                    'change_rate': float(row['涨跌幅']),
                    'market': 'SH' if row['代码'].startswith('6') else 'SZ'
                })
            
            logger.info(f"搜索关键词 '{keyword}' 找到 {len(results)} 条结果")
            return results
            
        except Exception as e:
            logger.error(f"搜索股票失败: {str(e)}")
            return []
    
    def get_market_overview(self) -> Dict:
        """
        获取市场概览数据
        返回: 市场统计信息
        """
        if not AKSHARE_AVAILABLE:
            return self.mock_service.get_market_overview()
            
        try:
            # 获取上证指数
            sh_index = self._retry_request(ak.stock_zh_index_spot_em, symbol="sh000001")
            # 获取深证成指
            sz_index = self._retry_request(ak.stock_zh_index_spot_em, symbol="sz399001")
            
            overview = {
                'sh_index': None,
                'sz_index': None,
                'total_stocks': 0,
                'up_count': 0,
                'down_count': 0,
                'flat_count': 0
            }
            
            # 处理上证指数
            if sh_index is not None and not sh_index.empty:
                sh_data = sh_index.iloc[0]
                overview['sh_index'] = {
                    'name': sh_data['名称'],
                    'current': float(sh_data['最新价']),
                    'change_rate': float(sh_data['涨跌幅']),
                    'change_amount': float(sh_data['涨跌额'])
                }
            
            # 处理深证成指
            if sz_index is not None and not sz_index.empty:
                sz_data = sz_index.iloc[0]
                overview['sz_index'] = {
                    'name': sz_data['名称'],
                    'current': float(sz_data['最新价']),
                    'change_rate': float(sz_data['涨跌幅']),
                    'change_amount': float(sz_data['涨跌额'])
                }
            
            # 获取市场统计
            market_data = self._retry_request(ak.stock_zh_a_spot_em)
            if market_data is not None and not market_data.empty:
                overview['total_stocks'] = len(market_data)
                overview['up_count'] = len(market_data[market_data['涨跌幅'] > 0])
                overview['down_count'] = len(market_data[market_data['涨跌幅'] < 0])
                overview['flat_count'] = len(market_data[market_data['涨跌幅'] == 0])
            
            return overview
            
        except Exception as e:
            logger.error(f"获取市场概览失败: {str(e)}")
            return {}
