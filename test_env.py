print("Python 环境测试")
print("Python 版本:")
import sys
print(sys.version)

print("\n测试模块导入:")
try:
    import pyautogui
    print("✓ pyautogui 导入成功")
except Exception as e:
    print(f"✗ pyautogui 导入失败: {e}")

try:
    from pynput import keyboard
    print("✓ pynput 导入成功")
except Exception as e:
    print(f"✗ pynput 导入失败: {e}")

try:
    from volcenginesdkarkruntime import Ark
    print("✓ volcenginesdkarkruntime 导入成功")
except Exception as e:
    print(f"✗ volcenginesdkarkruntime 导入失败: {e}")

print("\n测试完成")