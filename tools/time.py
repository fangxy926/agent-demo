from langchain.tools import BaseTool, StructuredTool, tool
from datetime import datetime


@tool
def get_current_time() -> str:
    """
    Returns the current time. Use this for any questions
    regarding the current time. Input is an empty string and
    the current time is returned in a string format. Only use this function
    for the current time. Other time related questions should use another tool
    """
    return str(datetime.now())


if __name__ == '__main__':
    print(get_current_time())
