# 将输出写入文件
with open('test_output.txt', 'w', encoding='utf-8') as f:
    f.write('Hello World!\n')
    f.write('This is a test script\n')
    f.write(f'1 + 1 = {1 + 1}\n')
    f.write('Script completed successfully\n')

print("Output written to test_output.txt")