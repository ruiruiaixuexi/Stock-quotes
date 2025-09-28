#!/usr/bin/env python
"""
依赖安装脚本 - 解决Windows环境下的安装问题
"""

import subprocess
import sys
import os

def run_pip_install(packages):
    """安装Python包"""
    for package in packages:
        print(f"正在安装 {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} 安装成功")
        except subprocess.CalledProcessError as e:
            print(f"❌ {package} 安装失败: {e}")
            return False
    return True

def main():
    """主函数"""
    print("🔧 开始安装项目依赖...")
    
    # 升级pip
    print("📦 升级pip...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        print("✅ pip升级成功")
    except:
        print("⚠️ pip升级失败，继续安装...")
    
    # 按顺序安装包
    packages = [
        "Django==4.2.7",
        "djangorestframework==3.14.0", 
        "django-cors-headers==4.3.1",
        "pandas",
        "numpy",
        "requests",
        "python-dotenv",
        "akshare"
    ]
    
    if run_pip_install(packages):
        print("\n🎉 所有依赖安装完成！")
        
        # 验证安装
        print("\n🧪 验证安装...")
        try:
            import django
            print(f"✅ Django {django.get_version()}")
            
            import rest_framework
            print("✅ Django REST Framework")
            
            import pandas
            print(f"✅ Pandas {pandas.__version__}")
            
            import numpy
            print(f"✅ NumPy {numpy.__version__}")
            
            import akshare
            print("✅ AKShare")
            
            print("\n🚀 可以开始运行项目了！")
            print("运行命令:")
            print("  python manage.py makemigrations")
            print("  python manage.py migrate") 
            print("  python manage.py runserver")
            
        except ImportError as e:
            print(f"❌ 验证失败: {e}")
    else:
        print("\n❌ 依赖安装失败")

if __name__ == "__main__":
    main()

