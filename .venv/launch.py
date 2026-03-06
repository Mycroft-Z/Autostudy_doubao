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
from config import api_key, endpoint_id, base_path, QandA_path
from volcenginesdkarkruntime import Ark

# 创建 Ark 客户端，传入 api_key
client = Ark(api_key=api_key)
import mumu_info

is_paused = False

# 用于检测 F9 按键的函数
def is_f9_pressed():
    # 直接使用 pyautogui 来检测 F9 按键
    try:
        return pyautogui.is_pressed('f9')
    except:
        return False

def safe_get_window_position():
    try:
        return mumu_info.get_mumu_window_position()
    except Exception as e:
        print(f"窗口定位失败: {str(e)}")
        return (0, 0, 0, 0, None)

def on_press(key):
    try:
        global is_paused
        
        if key == keyboard.Key.f9:
            is_paused = not is_paused
            if is_paused:
                print("已暂停，按 F9 继续")
            else:
                print("已继续")
            return True
        
        if key in (keyboard.Key.f10, keyboard.Key.f11):
            # 定义一个列表，用于储存题目答案
            ans_list = []
            before_que = None  # 初始化为None
            while True:  # 无限循环直到满足终止条件
                time.sleep(1)
                
                # 如果暂停，继续等待
                if is_paused:
                    continue
                
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
                    print(f"处理失败: {str(e)}，继续尝试识别")
                    # 不跳过，继续尝试
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
                # print(f"当前image_path: {image_path}")
                # print(f"函数返回值: {result}")
                # print(f"当前题目: {current_question}, 前一次题目: {before_que}")

                # 检查解析是否成功
                parse_success = True
                if key == keyboard.Key.f10:
                    # 检查是否是解析失败的默认值
                    if process_question == "解析失败":
                        print("解析失败，不执行滑动操作")
                        parse_success = False
                    else:
                        print("题目识别完成，准备执行操作...")
                        ans = main.execute_process_que_click(
                            question_type, process_answers, matched_answers, px, py, width, height
                        )
                        ans_list.append(ans)
                else:
                    # 对于F11模式，检查返回值是否有效
                    if not current_question or "解析失败" in current_question:
                        print("解析失败，不执行滑动操作")
                        parse_success = False
                    else:
                        print("答案识别完成，准备滑动屏幕...")
                        if width > 0 and height > 0:
                            drag_x = px + width * 4/5
                            drag_y = py + height * 4/5
                            pyautogui.moveTo(drag_x, drag_y)
                            pyautogui.dragTo(px + width/5, drag_y, duration=0.5)
                            pyautogui.moveTo(px, py)
                        print("滑动完成")

                # 终止条件：连续两次解析成功且题目相同
                if parse_success and before_que is not None and current_question == before_que:
                    print("连续两次识别到相同题目，结束操作,答案如下")
                    for i in ans_list:
                        print(i)
                    break
                elif parse_success:
                    # 只有解析成功时才更新前一次题目
                    before_que = current_question  # 更新前一次题目
                # 解析失败时不更新 before_que，保持之前的成功结果
            return True  # 统一抑制事件

        elif key == keyboard.Key.f12:
            print("脚本已关闭")
            return False  # 停止监听器

    except Exception as e:
        print(f"发生未知错误: {str(e)}")
        return True  # 异常时继续监听

def start_listener():
    with keyboard.Listener(on_press=on_press, suppress=False) as listener:
        try:
            listener.join()
        except KeyboardInterrupt:
            listener.stop()

if __name__ == "__main__":
    print("启动脚本...")
    print("导入模块完成")
    print("后台监听已启动，按F9暂停/继续，按F12退出")
    try:
        start_listener()
    except Exception as e:
        print(f"监听器启动失败: {e}")
        import traceback
        traceback.print_exc()

#存在问题：坐标偏离点歪