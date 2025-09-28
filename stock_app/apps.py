from django.apps import AppConfig


class StockAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stock_app'
    verbose_name = '股票行情应用'
