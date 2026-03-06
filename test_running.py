# 测试脚本是否正常运行
import os
import time

# 创建一个标记文件
with open('script_running.txt', 'w', encoding='utf-8') as f:
    f.write(f'Script started at: {time.strftime("%Y-%m-%d %H:%M:%S")}\n')
    f.write('Script is running...\n')

# 模拟一些工作
time.sleep(2)

# 更新文件
with open('script_running.txt', 'a', encoding='utf-8') as f:
    f.write(f'Script completed at: {time.strftime("%Y-%m-%d %H:%M:%S")}\n')
    f.write('Script ran successfully!\n')

print("Script completed. Check script_running.txt for details.")