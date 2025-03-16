import mumu_info
import pyautogui
import pygetwindow as gw
import os
import main
import time

windows = gw.getAllTitles()

print(windows)
pox, poy, width, height, screenshot_path = mumu_info.get_mumu_window_position()
print(mumu_info.get_mumu_window_position())
A = main.encode_image(screenshot_path)
time.sleep(2)
pox, poy, width, height, screenshot_path = mumu_info.get_mumu_window_position()
B = main.encode_image(screenshot_path)
print(A)
print(B)
#A和B两个字符串从头开始有多少个连续相等的字符
if A == B:
    print("same")
else:
    print("different")

