#!/usr/bin/env python
"""
测试项目设置脚本
"""

def test_imports():
    """测试必要的包导入"""
    try:
        import django
        print(f"✅ Django {django.get_version()} - 已安装")
    except ImportError:
        print("❌ Django - 未安装")
        return False
    
    try:
        import rest_framework
        print(f"✅ Django REST Framework - 已安装")
    except ImportError:
        print("❌ Django REST Framework - 未安装")
        return False
    
    try:
        import corsheaders
        print(f"✅ Django CORS Headers - 已安装")
    except ImportError:
        print("❌ Django CORS Headers - 未安装")
        return False
    
    try:
        import akshare
        print(f"✅ AKShare - 已安装")
    except ImportError:
        print("❌ AKShare - 未安装")
        return False
    
    try:
        import pandas
        print(f"✅ Pandas {pandas.__version__} - 已安装")
    except ImportError:
        print("❌ Pandas - 未安装")
        return False
    
    return True

def test_django_setup():
    """测试Django设置"""
    import os
    import sys
    
    # 添加项目路径
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stock_project.settings')
        import django
        django.setup()
        
        from django.conf import settings
        print(f"✅ Django设置 - 已加载")
        print(f"   - DEBUG: {settings.DEBUG}")
        print(f"   - 数据库: {settings.DATABASES['default']['ENGINE']}")
        
        return True
    except Exception as e:
        print(f"❌ Django设置 - 加载失败: {e}")
        return False

def test_models():
    """测试模型导入"""
    try:
        from stock_app.models import Stock, StockPrice, StockRealtime
        print("✅ 数据模型 - 导入成功")
        return True
    except Exception as e:
        print(f"❌ 数据模型 - 导入失败: {e}")
        return False

def test_akshare():
    """测试AKShare功能"""
    try:
        from stock_app.akshare_service import AKShareService
        service = AKShareService()
        print("✅ AKShare服务 - 初始化成功")
        
        # 简单测试（不实际请求数据）
        print("   - 服务配置正常")
        return True
    except Exception as e:
        print(f"❌ AKShare服务 - 初始化失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🧪 股票行情系统 - 环境测试")
    print("=" * 50)
    
    tests = [
        ("包依赖", test_imports),
        ("Django配置", test_django_setup),
        ("数据模型", test_models),
        ("AKShare服务", test_akshare),
    ]
    
    passed = 0
    total = len(tests)
    
    for name, test_func in tests:
        print(f"\n📋 测试: {name}")
        try:
            if test_func():
                passed += 1
            else:
                print(f"   测试失败")
        except Exception as e:
            print(f"   测试异常: {e}")
    
    print(f"\n📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！项目可以启动")
        print("\n🚀 运行以下命令启动项目:")
        print("   python manage.py makemigrations")
        print("   python manage.py migrate")
        print("   python manage.py runserver")
    else:
        print("⚠️  部分测试失败，请检查环境配置")
        print("\n💡 建议:")
        print("   pip install Django djangorestframework django-cors-headers akshare pandas")

if __name__ == "__main__":
    main()
