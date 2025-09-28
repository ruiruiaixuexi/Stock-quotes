#!/usr/bin/env python
"""
简单API测试
"""

import requests
import json
import time

def test_api():
    """测试API"""
    base_url = "http://127.0.0.1:8000/api"
    
    print("🧪 测试API接口...")
    time.sleep(2)  # 等待服务器启动
    
    try:
        # 测试基本端点
        response = requests.get(f"{base_url}/test/", timeout=5)
        print(f"✅ 测试端点: {response.status_code}")
        
        # 测试市场概览
        response = requests.get(f"{base_url}/market/", timeout=5)
        print(f"📊 市场概览: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
        
        # 测试股票列表
        response = requests.get(f"{base_url}/list/", timeout=5)
        print(f"📋 股票列表: {response.status_code}")
        
        # 测试搜索
        response = requests.get(f"{base_url}/search/?q=平安", timeout=5)
        print(f"🔍 股票搜索: {response.status_code}")
        
        print("\n🎉 API测试完成！")
        print("🌐 访问 http://127.0.0.1:8000/ 查看前端页面")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    test_api()
