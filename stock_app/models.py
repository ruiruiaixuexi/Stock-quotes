from django.db import models
from django.utils import timezone


class Stock(models.Model):
    """股票基本信息模型"""
    code = models.CharField(max_length=10, unique=True, verbose_name='股票代码')
    name = models.CharField(max_length=100, verbose_name='股票名称')
    market = models.CharField(max_length=10, default='SH', verbose_name='市场')
    industry = models.CharField(max_length=100, blank=True, verbose_name='所属行业')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'stock_info'
        verbose_name = '股票信息'
        verbose_name_plural = '股票信息'
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.name}"


class StockPrice(models.Model):
    """股票价格数据模型"""
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='prices', verbose_name='股票')
    date = models.DateField(verbose_name='交易日期')
    open_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='开盘价')
    high_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='最高价')
    low_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='最低价')
    close_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='收盘价')
    volume = models.BigIntegerField(verbose_name='成交量')
    amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='成交额')
    change_rate = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name='涨跌幅(%)')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'stock_price'
        verbose_name = '股票价格'
        verbose_name_plural = '股票价格'
        unique_together = ['stock', 'date']
        ordering = ['-date']

    def __str__(self):
        return f"{self.stock.code} - {self.date} - {self.close_price}"

    @property
    def change_amount(self):
        """计算涨跌金额"""
        if self.change_rate:
            return float(self.close_price) * float(self.change_rate) / 100
        return 0


class StockRealtime(models.Model):
    """实时股票数据模型"""
    stock = models.OneToOneField(Stock, on_delete=models.CASCADE, related_name='realtime', verbose_name='股票')
    current_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='当前价格')
    change_rate = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='涨跌幅(%)')
    change_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='涨跌金额')
    volume = models.BigIntegerField(verbose_name='成交量')
    amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='成交额')
    high_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='今日最高')
    low_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='今日最低')
    open_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='今日开盘')
    pre_close = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='昨日收盘')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'stock_realtime'
        verbose_name = '实时行情'
        verbose_name_plural = '实时行情'

    def __str__(self):
        return f"{self.stock.code} - 实时价格: {self.current_price}"
