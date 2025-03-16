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

def on_press(key):
    try:
        if key in (keyboard.Key.f10, keyboard.Key.f11):
            # 独占处理：无论操作是否成功，均抑制事件传递
            if key == keyboard.Key.f10:
                before_que = 1
                while True:
                    # 循环答题，直到本次识别的题目与上次相同
                    time.sleep(1)
                    pox, pox, width, height, image_path = mumu_info.get_mumu_window_position()
                    question_type, process_question, process_answers, matched_answers = main.execute_process_que(
                        image_path, client, endpoint_id, QandA_path)
                    if process_question != before_que:
                        main.execute_process_que_click(question_type, process_answers, matched_answers, pox, pox, width, height)
                        before_que = process_question
                    else:
                        print("本次识别的题目与上次相同，结束答题")
                        break

            if key == keyboard.Key.f11:
                before_que = 1
                while True:
                    time.sleep(1)
                    # 循环记题，直到本次识别的题目与上次相同
                    pox, poy, width, height, image_path = mumu_info.get_mumu_window_position()
                    process_question = main.execute_process_ans(
                        image_path, client, endpoint_id, QandA_path
                    )
                    if process_question == before_que:
                        print("本次识别的题目与上次相同，结束记题")
                        break
                    else:
                        before_que = process_question
                        # 执行拖拽操作（示例使用 pyautogui 的 dragTo）
                        pyautogui.moveTo(pox + width * 4 / 5, poy + height * 4 / 5)
                        pyautogui.dragTo(pox + width / 5, poy + height * 4 / 5, duration=0.5)
                        # 将鼠标移动到原点，防止干扰下一题识别
                        pyautogui.moveTo(pox, poy)


            return True  # 统一抑制F10/F11事件传递

        elif key == keyboard.Key.f12:
            print("脚本已关闭")
            return False  # 停止监听器

    except Exception as e:
        print(f"发生未知错误: {str(e)}")
        return True  # 其他异常也抑制事件传递

def start_listener():
    # 设置`suppress=True`可增强事件抑制（某些系统可能需要）
    with keyboard.Listener(on_press=on_press, suppress=True) as listener:
        try:
            listener.join()
        except KeyboardInterrupt:
            listener.stop()

if __name__ == "__main__":
    print("后台监听已启动，按F12退出")
    start_listener()
