import base64
from volcenginesdkarkruntime import Ark
import pandas as pd
import pyautogui
import time
import pygetwindow as gw
import os
import excel_write
from config import api_key,endpoint_id,base_path,QandA_path


# 创建 Ark 客户端，传入 api_key
client = Ark(api_key=api_key)

# 图片编码
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
# 答案页面识别，输出[题目,正确选项1内容,正确选项2内容…]
def process_image_and_request_ans(image_path, client, endpoint_id):
    try:
        # 编码图片
        image_base64 = encode_image(image_path)

        # 发送请求
        print("----- standard request -----")
        completion = client.chat.completions.create(
            model=endpoint_id,
            messages=[
                {"role": "system", "content": "你是AI图像识别助手，按照我的要求输出答案"},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "从图片中提取出页面类型、题目类型、题目、正确选项内容,输出为python列表格式。例：[查看答卷，判断题，题目,正确选项1内容,正确选项2内容]"},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_base64}"}}

                    ]
                }
            ]
        )
        # 打印响应结果
        return(completion.choices[0].message.content)
    except Exception as e:
        print(f"请求过程中出现错误: {e}")
# 答题页面识别，输出[题目,{A选项内容:(A选项横坐标，A选项纵坐标)},{B选项内容:(B选项横坐标，B选项纵坐标)}]
def process_image_and_request_que(image_path, client, endpoint_id):
    try:
        # 编码图片
        image_base64 = encode_image(image_path)

        # 发送请求
        print("----- standard request -----")
        completion = client.chat.completions.create(
            model=endpoint_id,
            messages=[
                {"role": "system", "content": "你是AI图像识别助手，按照我的要求输出答案"},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "从图片中提取出页面类型、题目类型、题目、选项、选项所在的像素坐标。原点为图片左上角，输出为python列表格式，其中选项内容与坐标互为键值对，坐标为元组格式且只包含两个数字。例：[考试作答、判断题、题目,{A选项内容:(A选项横坐标，A选项纵坐标),B选项内容:(B选项横坐标，B选项纵坐标)}]"},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_base64}"}}
                    ]
                }
            ]
        )
        # 打印响应结果
        return(completion.choices[0].message.content)
    except Exception as e:
        print(f"请求过程中出现错误: {e}")

# 在excel中匹配答案，输出[题目,正确选项1内容,正确选项2内容…]
def match_question_in_excel(question, excel_path, sheet_name='Sheet1', question_column='题目'):
    try:
        # 读取Excel文件，使用相对路径
        df = pd.read_excel(excel_path, sheet_name=sheet_name)

        # 匹配题目
        matched_row = df[df[question_column] == question]

        if not matched_row.empty:
            # 过滤空值
            non_empty_values = matched_row.iloc[0].dropna().tolist()
            return non_empty_values
        else:
            return []
    except Exception as e:
        print(f"匹配过程中出现错误: {e}")
        return []


#答题执行部分
def execute_process_que(image_path, client, endpoint_id,QandA_path,):
    question_type,process_question,process_answers = eval(process_image_and_request_que(image_path, client, endpoint_id))[1:4]
    print(process_question,process_answers)
    print(type(process_question),type(process_answers))
    matched_answers = match_question_in_excel(process_question, QandA_path)[1:]
    print(matched_answers)
    return question_type, process_question, process_answers, matched_answers

#如果匹配到题目则执行元素点击操作
def execute_process_que_click(question_type, process_answers, matched_answers, pox, poy, width, height):
    if matched_answers != []:
        print("匹配到题目")
        print(matched_answers)
        print(type(matched_answers))
        #依次以列表matched_answers中的元素作为key 点击process_answers中的value
        for key in matched_answers:
            click_position_x , click_position_y = process_answers[str(key)]
            pyautogui.click(click_position_x + pox, click_position_y + poy + 30)
    else:
        first_key = next(iter(process_answers))
        click_position_x, click_position_y = process_answers[first_key]
        pyautogui.click(click_position_x + pox, click_position_y + poy + 30)
        print('不在题库中')

    # 如果是多选题，则进行滑动操作进入下一题
    if question_type == '多选题':
        # 执行拖拽操作（示例使用 pyautogui 的 dragTo）
        pyautogui.moveTo(pox + width * 4 / 5, poy + height * 4 / 5)
        pyautogui.dragTo(pox + width / 5, poy + height * 4 / 5, duration=0.5)
    # 将鼠标移动到原点，防止干扰下一题识别
    pyautogui.moveTo(pox, poy)

#答案记录部分
def execute_process_ans(image_path, client, endpoint_id,QandA_path):
    process_question = eval(process_image_and_request_ans(image_path, client, endpoint_id))
    #将识别的题目和答案内容写入excel，先判断是否有匹配的题目，如果有则不写入，如果没有则写入
    matched_question = match_question_in_excel(process_question[2], QandA_path)
    print(process_question)
    if matched_question != []:
         print("题库重复，无需写入")
         pass
    else:
         # 如果未匹配到题目则写入
         excel_write.append_list_to_excel(QandA_path, process_question[2:])
         print("已写入题库")
    return process_question[2]

