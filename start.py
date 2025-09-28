#!/usr/bin/env python
"""
股票行情系统启动脚本
自动安装依赖并启动Django开发服务器
"""

import os
import sys
import subprocess
import platform

def run_command(command, description):
    """执行命令并显示进度"""
    print(f"\n🔄 {description}...")
    try:
        if platform.system() == "Windows":
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        else:
            result = subprocess.run(command.split(), check=True, capture_output=True, text=True)
        
        if result.stdout:
            print(f"✅ {description}完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description}失败: {e}")
        if e.stdout:
            print(f"输出: {e.stdout}")
        if e.stderr:
            print(f"错误: {e.stderr}")
        return False

def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ 需要Python 3.8或更高版本")
        return False
    print(f"✅ Python版本: {version.major}.{version.minor}.{version.micro}")
    return True

def install_dependencies():
    """安装项目依赖"""
    dependencies = [
        "Django>=4.2.0",
        "djangorestframework>=3.14.0", 
        "django-cors-headers>=4.0.0",
        "akshare>=1.12.0",
        "pandas>=2.0.0"
    ]
    
    print("📦 安装项目依赖...")
    for dep in dependencies:
        if not run_command(f"pip install {dep}", f"安装 {dep}"):
            return False
    return True

def setup_database():
    """设置数据库"""
    commands = [
        ("python manage.py makemigrations", "创建数据库迁移文件"),
        ("python manage.py migrate", "执行数据库迁移")
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    return True

def start_server():
    """启动开发服务器"""
    print("\n🚀 启动Django开发服务器...")
    print("📱 访问地址: http://127.0.0.1:8000/")
    print("🔧 管理后台: http://127.0.0.1:8000/admin/")
    print("📊 API接口: http://127.0.0.1:8000/api/")
    print("\n按 Ctrl+C 停止服务器\n")
    
    try:
        subprocess.run("python manage.py runserver", shell=True, check=True)
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
    except subprocess.CalledProcessError as e:
        print(f"❌ 启动服务器失败: {e}")

def main():
    """主函数"""
    print("🏠 股票行情系统启动器")
    print("=" * 50)
    
    # 检查Python版本
    if not check_python_version():
        return
    
    # 检查是否在项目目录
    if not os.path.exists("manage.py"):
        print("❌ 请在项目根目录运行此脚本")
        return
    
    # 安装依赖
    if not install_dependencies():
        print("❌ 依赖安装失败，请手动安装")
        return
    
    # 设置数据库
    if not setup_database():
        print("❌ 数据库设置失败")
        return
    
    # 启动服务器
    start_server()

if __name__ == "__main__":
    main()
