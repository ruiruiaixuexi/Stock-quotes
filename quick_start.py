#!/usr/bin/env python
"""
快速启动脚本 - 修复并启动项目
"""

import os
import sys
import subprocess

def run_command(command, description):
    """执行命令"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description}完成")
        if result.stdout:
            print(f"输出: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description}失败")
        if e.stderr:
            print(f"错误: {e.stderr.strip()}")
        return False

def main():
    """主函数"""
    print("🚀 股票行情系统 - 快速启动")
    print("=" * 50)
    
    # 检查Django
    if not run_command("python -c \"import django; print('Django OK')\"", "检查Django"):
        print("请先安装Django: pip install Django")
        return
    
    # 检查项目配置
    if not run_command("python manage.py check --deploy", "检查项目配置"):
        print("项目配置有问题，尝试基本检查...")
        if not run_command("python manage.py check", "基本配置检查"):
            return
    
    # 创建迁移
    run_command("python manage.py makemigrations stock_app", "创建应用迁移")
    
    # 执行迁移
    if not run_command("python manage.py migrate", "执行数据库迁移"):
        return
    
    # 收集静态文件
    run_command("python manage.py collectstatic --noinput", "收集静态文件")
    
    print("\n🎉 项目准备完成！")
    print("\n🌐 访问地址:")
    print("   前端页面: http://127.0.0.1:8000/")
    print("   API接口: http://127.0.0.1:8000/api/")
    print("   管理后台: http://127.0.0.1:8000/admin/")
    
    print("\n🚀 启动开发服务器...")
    print("按 Ctrl+C 停止服务器")
    
    try:
        subprocess.run("python manage.py runserver", shell=True, check=True)
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")

if __name__ == "__main__":
    main()

