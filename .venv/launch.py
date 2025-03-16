from pynput import keyboard
import sys
import main
import base64
from volcenginesdkarkruntime import Ark
import pandas as pd
import pyautogui
import time
import pygetwindow as gw
import os
import excel_write
from config import api_key, endpoint_id, base_path, QandA_path, client
import mumu_info

def safe_get_window_position():
    try:
        return mumu_info.get_mumu_window_position()
    except Exception as e:
        print(f"窗口定位失败: {str(e)}")
        return (0, 0, 0, 0, None)

def on_press(key):
    try:
        if key in (keyboard.Key.f10, keyboard.Key.f11):
            before_que = None  # 初始化为None
            while True:  # 无限循环直到满足终止条件
                time.sleep(1)
                px, py, width, height, image_path = safe_get_window_position()

                if image_path is None:
                    print("窗口定位失败，跳过本次处理")
                    continue  # 跳过本次循环，继续下次尝试

                if key == keyboard.Key.f10:
                    func = main.execute_process_que
                    args = (image_path, client, endpoint_id, QandA_path)
                else:
                    func = main.execute_process_ans
                    args = (image_path, client, endpoint_id, QandA_path)

                try:
                    result = func(*args)
                except Exception as e:
                    print(f"处理失败: {str(e)}，跳过本次处理")
                    continue

                # 强制检查返回值类型
                if not result:
                    print(result)
                    print(type(result))
                    print("未获取到有效题目内容，跳过本次处理")
                    continue

                if key == keyboard.Key.f10:
                    question_type, process_question, process_answers, matched_answers = result
                    current_question = process_question
                else:
                    # 明确指定F11分支返回的题目内容
                    current_question = result  # 假设execute_process_ans返回题目字符串

                # 调试输出增强：显示image_path和返回值
                print(f"当前image_path: {image_path}")
                print(f"函数返回值: {result}")
                print(f"当前题目: {current_question}, 前一次题目: {before_que}")

                # 终止条件：连续两次题目相同且非None
                if before_que is not None and current_question == before_que:
                    print("连续两次识别到相同题目，结束操作")
                    break
                else:
                    before_que = current_question  # 更新前一次题目

                # 执行操作（答题或拖拽）
                if key == keyboard.Key.f10:
                    main.execute_process_que_click(
                        question_type, process_answers, matched_answers, px, py, width, height
                    )
                else:
                    if width > 0 and height > 0:
                        drag_x = px + width * 4/5
                        drag_y = py + height * 4/5
                        pyautogui.moveTo(drag_x, drag_y)
                        pyautogui.dragTo(px + width/5, drag_y, duration=0.5)
                        pyautogui.moveTo(px, py)
            return True  # 统一抑制事件

        elif key == keyboard.Key.f12:
            print("脚本已关闭")
            return False  # 停止监听器

    except Exception as e:
        print(f"发生未知错误: {str(e)}")
        return True  # 异常时继续监听

def start_listener():
    with keyboard.Listener(on_press=on_press, suppress=True) as listener:
        try:
            listener.join()
        except KeyboardInterrupt:
            listener.stop()

if __name__ == "__main__":
    print("后台监听已启动，按F12退出")
    start_listener()
