
# 调用 cmd 命令行执行 allure 生成测试报告的命令
import os
import subprocess
import sys
import shutil
import platform


def check_allure_installed():
    """检查 allure 是否安装并返回完整路径"""
    print("正在检查allure安装状态...")
    
    # 方法 1: 尝试直接使用 allure 命令
    try:
        print("尝试直接运行allure命令...")
        result = subprocess.run(['allure', '--version'], capture_output=True, text=True)
        print(f"allure命令返回码: {result.returncode}")
        if result.returncode == 0:
            print(f"✓ allure 已安装：{result.stdout.strip()}")
            return 'allure'  # 返回命令字符串而不是True
        else:
            print(f"allure命令失败，错误信息: {result.stderr}")
    except FileNotFoundError:
        print("✗ allure命令未找到")
    except Exception as e:
        print(f"✗ 执行allure命令时发生错误: {e}")
    
    # 方法 2: 从PATH环境变量中搜索allure
    print("正在从PATH环境变量中搜索allure...")
    path_env = os.environ.get('PATH', '')
    path_dirs = path_env.split(os.pathsep)
    
    # 搜索allure相关的可执行文件
    allure_files = ['allure', 'allure.bat', 'allure.cmd']
    
    for path_dir in path_dirs:
        for allure_file in allure_files:
            full_path = os.path.join(path_dir, allure_file)
            if os.path.exists(full_path) and os.path.isfile(full_path):
                print(f"在PATH中找到: {full_path}")
                # 验证是否可执行
                try:
                    result = subprocess.run([full_path, '--version'], capture_output=True, text=True, timeout=5)
                    if result.returncode == 0:
                        print(f"✓ PATH中的allure可用: {result.stdout.strip()}")
                        return full_path
                    else:
                        print(f"✗ PATH中的allure不可用: {result.stderr}")
                except Exception as e:
                    print(f"✗ 测试PATH中的allure时发生错误: {e}")
    
    # 方法 3: 在 Windows 上尝试常见安装路径
    if platform.system() == 'Windows':
        print("正在检查Windows常见安装路径...")
        common_paths = [
            # 您的实际安装路径（尝试多种可能的文件名）
            r'D:llurellure-2.38.0inllure.bat',
            r'D:llurellure-2.38.0inllure',
            r'D:llurellure-2.38.0inllure.cmd',
            # 其他常见安装路径
            os.path.expandvars(r'%APPDATA%pmllure.bat'),
            os.path.expandvars(r'%APPDATA%pmllure'),
            os.path.expandvars(r'%APPDATA%pmllure.cmd'),
            os.path.expandvars(r'%USERPROFILE%coopppsllureurrentinllure.bat'),
            r'C:rogramDatahocolateyinllure.bat',
        ]
        
        for allure_path in common_paths:
            print(f"检查路径: {allure_path}")
            if os.path.exists(allure_path):
                print(f"✓ 找到 allure: {allure_path}")
                # 验证该路径是否可执行
                try:
                    result = subprocess.run([allure_path, '--version'], capture_output=True, text=True, timeout=5)
                    if result.returncode == 0:
                        print(f"✓ 路径可执行: {result.stdout.strip()}")
                        return allure_path
                    else:
                        print(f"✗ 路径不可执行: {result.stderr}")
                except Exception as e:
                    print(f"✗ 执行路径时发生错误: {e}")
            else:
                print(f"✗ 路径不存在")
    
    print("✗ 未找到可用的allure安装")
    return False


def generate_report():
    """生成 Allure 测试报告"""
    # 检查 allure 命令行工具是否可用
    allure_cmd = check_allure_installed()
    
    if not allure_cmd:
        print("✗ allure 命令行工具未安装或不可用")
        print("\n请按照以下步骤安装:")
        print("=" * 60)
        print("方法 1: 使用 npm (推荐)")
        print("  npm install -g allure-commandline")
        print("\n方法 2: 使用 scoop")
        print("  scoop install allure")
        print("\n方法 3: 使用 chocolatey")
        print("  choco install allure")
        print("\n方法 4: 手动下载")
        print("  https://github.com/allure-framework/allure2/releases")
        print("\n安装后请确保 allure 命令在 PATH 中:")
        print("  allure --version")
        print("=" * 60)
        
        # 尝试提供有用的诊断信息
        print("\n诊断信息:")
        print(f"  Python 路径：{sys.executable}")
        print(f"  当前目录：{os.getcwd()}")
        print(f"  PATH 长度：{len(os.environ.get('PATH', ''))} 字符")
        
        # 检查是否在虚拟环境中
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            print(f"  虚拟环境：{sys.prefix}")
        
        return
    
    # 如果 check_allure_installed 返回的是完整路径，使用它；否则使用 'allure'
    if isinstance(allure_cmd, str) and os.path.exists(allure_cmd):
        ALLURE_CMD = allure_cmd
    else:
        ALLURE_CMD = 'allure'
    
    print(f"使用 allure 命令：{ALLURE_CMD}")
    
    try:
        # 统一使用 allure-results 目录（标准做法）
        allure_results_dir = './allure-results'
        report_html_dir = './report/html'
        
        # 清理旧报告
        if os.path.exists(allure_results_dir):
            shutil.rmtree(allure_results_dir)
            print(f"已清理旧的 allure-results 目录")
        
        if os.path.exists(report_html_dir):
            shutil.rmtree(report_html_dir)
            print(f"已清理旧的 HTML 报告目录")
        
        # 创建新的 allure-results 目录
        os.makedirs(allure_results_dir, exist_ok=True)
        
        print("正在运行测试并生成 allure 数据...")
        # 使用 pytest 运行测试并生成 allure 数据
        # 注意：不使用 pytest.ini 的配置，完全用命令行参数覆盖
        pytest_result = subprocess.run([
            sys.executable, '-m', 'pytest',
            'script/',  # 只测试 script 目录
            f'--alluredir={allure_results_dir}',
            '--clean-alluredir',
            '-v',  # 显示详细信息
            '-s',  # 显示 print 输出
            '--tb=short'  # 简化错误追踪
        ], capture_output=True, text=True)  # 改为捕获输出以获取错误信息
        
        # 显示测试输出
        print("\n=== 测试执行输出 ===")
        print(pytest_result.stdout)
        if pytest_result.stderr:
            print("STDERR:", pytest_result.stderr)
        
        if pytest_result.returncode != 0:
            print(f"\n✗ 测试执行失败，返回码：{pytest_result.returncode}")
            # 即使测试失败，也尝试生成已有的报告
            if not os.listdir(allure_results_dir):
                print("allure-results 目录为空，无法生成报告")
                return
        
        # 检查是否有测试结果
        result_files = os.listdir(allure_results_dir)
        if not result_files:
            print("✗ allure-results 目录中没有测试结果文件")
            return
        
        print(f"\n✓ 测试执行完成，找到 {len(result_files)} 个结果文件")
        print("正在生成 HTML 报告...")
        
        # 方法 1: 使用 allure generate 生成静态报告
        gen_result = subprocess.run([
            ALLURE_CMD, 'generate',
            allure_results_dir,
            '-o', report_html_dir,
            '--clean'
        ], capture_output=True, text=True)
        
        if gen_result.returncode != 0:
            print(f"✗ allure generate 失败:")
            print(gen_result.stderr)
            # 尝试使用 allure serve 直接打开
            print("\n尝试使用 allure serve 直接查看报告...")
            subprocess.run([
                ALLURE_CMD, 'serve',
                allure_results_dir
            ])
            return
        
        print("✓ 测试报告生成成功！")
        print(f"报告路径：{os.path.abspath(report_html_dir)}")
        print(f"\n提示：可以使用以下命令查看报告:")
        print(f"  allure serve {allure_results_dir}")
        print(f"  或者打开：{os.path.join(report_html_dir, 'index.html')}")
        
    except FileNotFoundError as e:
        print(f"\n✗ 命令未找到：{e}")
        print("\n请确认:")
        print("  1. allure-pytest 已安装：pip install allure-pytest")
        print(f"  2. allure 命令行工具已安装并可访问：{ALLURE_CMD}")
    except Exception as e:
        print(f"\n✗ 发生错误：{e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    generate_report()