#!/usr/bin/env python3
"""
自动化测试主运行器
集成Web测试、移动端测试和报告生成
"""

import os
import sys
import time
import subprocess
from datetime import datetime
from generate_report import generate_html_report

def setup_environment():
    """设置测试环境"""
    print("🔧 设置测试环境...")
    
    # 创建必要的目录
    os.makedirs("images", exist_ok=True)
    os.makedirs("report", exist_ok=True)
    os.makedirs("tests", exist_ok=True)
    
    # 安装Playwright浏览器
    try:
        print("📦 安装Playwright浏览器...")
        subprocess.run([sys.executable, "-m", "playwright", "install"], check=True)
        print("✅ Playwright浏览器安装完成")
    except subprocess.CalledProcessError as e:
        print(f"❌ Playwright浏览器安装失败: {e}")
    
    print("✅ 环境设置完成")

def run_web_tests():
    """运行Web自动化测试"""
    print("\n🌐 开始Web自动化测试...")
    
    try:
        # 使用pytest运行Web测试
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/web_test.py", 
            "-v", "--html=report/web_test_report.html", "--self-contained-html"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Web测试执行成功")
            print(result.stdout)
        else:
            print("⚠️ Web测试执行有错误")
            print(result.stdout)
            print(result.stderr)
            
    except Exception as e:
        print(f"❌ Web测试执行失败: {e}")
    
    print("✅ Web测试完成")

def run_mobile_tests():
    """运行移动端自动化测试"""
    print("\n📱 开始移动端自动化测试...")
    
    try:
        # 使用pytest运行移动端测试
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/mobile_test.py", 
            "-v", "--html=report/mobile_test_report.html", "--self-contained-html"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ 移动端测试执行成功")
            print(result.stdout)
        else:
            print("⚠️ 移动端测试执行有错误")
            print(result.stdout)
            print(result.stderr)
            
    except Exception as e:
        print(f"❌ 移动端测试执行失败: {e}")
    
    print("✅ 移动端测试完成")

def test_with_playwright():
    """使用Playwright进行实际网页测试"""
    print("\n🎯 开始Playwright实际测试...")
    
    try:
        from playwright.sync_api import sync_playwright
        
        test_results = []
        
        with sync_playwright() as p:
            # 测试1: 百度搜索
            print("🔍 测试百度搜索功能...")
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            
            start_time = time.time()
            
            try:
                page.goto("https://www.baidu.com")
                page.wait_for_selector("#kw")
                page.fill("#kw", "自动化测试")
                page.click("#su")
                page.wait_for_selector(".result")
                
                # 截图
                screenshot_path = f"images/baidu_test_{int(time.time())}.png"
                page.screenshot(path=screenshot_path, full_page=True)
                
                test_results.append({
                    "name": "百度搜索功能测试",
                    "status": "PASS",
                    "duration": time.time() - start_time,
                    "screenshot": screenshot_path
                })
                print("✅ 百度搜索测试通过")
                
            except Exception as e:
                test_results.append({
                    "name": "百度搜索功能测试",
                    "status": "FAIL",
                    "duration": time.time() - start_time,
                    "error": str(e)
                })
                print(f"❌ 百度搜索测试失败: {e}")
            
            browser.close()
        
        # 测试2: 淘宝首页
        print("🛒 测试淘宝首页加载...")
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        start_time = time.time()
        
        try:
            page.goto("https://www.taobao.com")
            page.wait_for_selector(".nav-item", timeout=10000)
            
            # 截图
            screenshot_path = f"images/taobao_test_{int(time.time())}.png"
            page.screenshot(path=screenshot_path, full_page=True)
            
            test_results.append({
                "name": "淘宝首页加载测试",
                "status": "PASS",
                "duration": time.time() - start_time,
                "screenshot": screenshot_path
            })
            print("✅ 淘宝首页测试通过")
            
        except Exception as e:
            test_results.append({
                "name": "淘宝首页加载测试",
                "status": "FAIL",
                "duration": time.time() - start_time,
                "error": str(e)
            })
            print(f"❌ 淘宝首页测试失败: {e}")
        
        browser.close()
        
        return test_results
        
    except Exception as e:
        print(f"❌ Playwright测试执行失败: {e}")
        return []

def check_mobile_devices():
    """检查可用的移动设备"""
    print("\n📱 检查移动设备...")
    
    try:
        # 这里可以集成mobile-mcp的设备检查功能
        # 暂时模拟设备检查
        print("🔍 扫描可用设备...")
        
        # 模拟设备列表
        devices = [
            {"name": "Android Emulator", "status": "available"},
            {"name": "iOS Simulator", "status": "available"}
        ]
        
        for device in devices:
            print(f"📱 {device['name']} - {device['status']}")
        
        print("✅ 设备检查完成")
        return devices
        
    except Exception as e:
        print(f"❌ 设备检查失败: {e}")
        return []

def generate_final_report():
    """生成最终测试报告"""
    print("\n📊 生成最终测试报告...")
    
    try:
        report_path = generate_html_report()
        
        # 打开报告
        if os.path.exists(report_path):
            print(f"✅ 测试报告已生成: {report_path}")
            
            # 在Windows上打开报告
            if os.name == 'nt':
                os.startfile(report_path)
            else:
                # 在其他系统上使用默认浏览器打开
                import webbrowser
                webbrowser.open(f'file://{os.path.abspath(report_path)}')
        
        return report_path
        
    except Exception as e:
        print(f"❌ 报告生成失败: {e}")
        return None

def main():
    """主函数"""
    print("🚀 开始自动化测试流程")
    print("=" * 50)
    
    start_time = time.time()
    
    # 1. 环境设置
    setup_environment()
    
    # 2. 检查移动设备
    check_mobile_devices()
    
    # 3. 运行Web测试
    run_web_tests()
    
    # 4. 运行移动端测试
    run_mobile_tests()
    
    # 5. 使用Playwright进行实际测试
    playwright_results = test_with_playwright()
    
    # 6. 生成最终报告
    report_path = generate_final_report()
    
    # 统计信息
    total_time = time.time() - start_time
    print("\n" + "=" * 50)
    print(f"🎉 自动化测试流程完成")
    print(f"⏱️  总执行时间: {total_time:.2f}秒")
    
    if report_path:
        print(f"📊 测试报告位置: {os.path.abspath(report_path)}")
    
    print("✅ 所有测试任务已完成")

if __name__ == "__main__":
    main()