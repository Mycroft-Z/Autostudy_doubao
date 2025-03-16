import pyautogui
import pygetwindow as gw
import os

def get_mumu_window_position():
    # 获取所有窗口
    windows = gw.getAllTitles()

    # 查找MUMU模拟器的窗口标题
    mumu_title = None
    for title in windows:
        if "MuMu" in title:
            mumu_title = title
            break

    if mumu_title:
        # 获取窗口对象
        mumu_window = gw.getWindowsWithTitle(mumu_title)[0]

        # 激活窗口
        mumu_window.activate()

        # 获取窗口坐标
        left, top, width, height = mumu_window.left, mumu_window.top, mumu_window.width, mumu_window.height

        # 捕获窗口截图
        screenshot = pyautogui.screenshot(region=(left, top, width, height))

        # 保存截图到lib目录
        screenshot_path = os.path.join('lib', 'mumu_screenshot.png')
        screenshot.save(screenshot_path)

        return left, top, width, height, screenshot_path
    else:
        print("未找到MUMU模拟器窗口")
        return None

