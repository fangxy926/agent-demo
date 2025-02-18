from langchain.tools import tool
from datetime import datetime
import pytz


@tool
def get_current_time(input: str) -> str:
    """
    返回当前时间。用于处理与当前时间相关的问题。
    仅用于获取当前时间，其他与时间相关的问题应使用其他工具。
    """
    tz = pytz.timezone('Asia/ShangHai')  # 设置时区为台北
    current_time = datetime.now(tz)
    return current_time.strftime("%Y-%m-%d %H:%M:%S")


if __name__ == '__main__':
    print(get_current_time.invoke(""))
