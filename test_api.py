#!/usr/bin/env python
"""
API测试脚本
"""

import requests
import json
import time

def test_api_endpoint(url, description):
    """测试API端点"""
    try:
        print(f"🔍 测试: {description}")
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {description} - 成功")
            print(f"   状态码: {response.status_code}")
            if isinstance(data, list):
                print(f"   数据条数: {len(data)}")
            elif isinstance(data, dict):
                print(f"   数据键: {list(data.keys())}")
            return True
        else:
            print(f"❌ {description} - 失败")
            print(f"   状态码: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ {description} - 连接失败: {e}")
        return False
    except Exception as e:
        print(f"❌ {description} - 异常: {e}")
        return False

def main():
    """主测试函数"""
    print("🧪 API接口测试")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:8000"
    
    # 等待服务器启动
    print("⏳ 等待服务器启动...")
    time.sleep(3)
    
    # 测试端点列表
    endpoints = [
        (f"{base_url}/", "主页面"),
        (f"{base_url}/api/market/", "市场概览"),
        (f"{base_url}/api/list/", "股票列表"),
        (f"{base_url}/api/search/?q=平安", "股票搜索"),
        (f"{base_url}/api/stocks/000001/", "股票详情"),
        (f"{base_url}/api/stocks/000001/realtime/", "实时行情"),
        (f"{base_url}/api/stocks/000001/history/", "历史数据"),
    ]
    
    passed = 0
    total = len(endpoints)
    
    for url, description in endpoints:
        if test_api_endpoint(url, description):
            passed += 1
        print()  # 空行分隔
    
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有API测试通过！")
        print(f"\n🌐 访问地址:")
        print(f"   前端页面: {base_url}/")
        print(f"   API接口: {base_url}/api/")
    else:
        print("⚠️ 部分API测试失败")
        
    print(f"\n💡 提示: 当前使用模拟数据，如需真实数据请安装AKShare")

if __name__ == "__main__":
    main()

