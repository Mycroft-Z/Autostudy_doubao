from openpyxl import load_workbook

def append_list_to_excel(file_path, data_list, sheet_name='Sheet1'):
    """
    将列表内容追加到Excel文件的第一个空行，后台运行不打开文件

    Args:
        file_path (str): Excel文件路径
        data_list (list): 需要写入的数据列表（每个元素对应一列）
        sheet_name (str, optional): 工作表名称，默认使用活动表
    """
    # 加载现有工作簿
    wb = load_workbook(file_path)
    ws = wb.active if sheet_name is None else wb[sheet_name]

    # 获取第一个空行位置（当前最后非空行+1）
    next_row = ws.max_row + 1 if ws.max_row > 0 else 1

    # 写入数据到连续列
    for col_idx, value in enumerate(data_list, 1):
        ws.cell(row=next_row, column=col_idx, value=value)

    # 保存修改（不会打开Excel程序）
    wb.save(file_path)

