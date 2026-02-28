from volcenginesdkarkruntime import Ark
import os

# volcenginesdkarkruntime安装： 1、将python目录加入环境变量 2、pip install volcengine-python-sdk[ark]


# 获取当前脚本所在的项目根目录
project_root = os.path.dirname(os.path.abspath(__file__))

# 构建相对路径（使用 os.path.join 确保跨平台兼容性）
base_path = os.path.join(project_root, "Lib", "picture_ques")
QandA_path = os.path.join(project_root, "Lib", "QandA.xlsx")


# 从环境变量中获取 API 密钥和 Endpoint ID（提高安全性）
api_key = os.getenv("VOLC_API_KEY", "ce3dffd6-f12a-4cf5-a1a2-fbb476ed302e")
endpoint_id = os.getenv("VOLC_ENDPOINT_ID", "ep-20251018011736-hplwm")

# 初始化客户端
client = Ark(api_key=api_key)