from langchain.tools import tool
from datetime import datetime


@tool
def get_current_time(input: str) -> str:
    """
    Returns the current time. Use this for any questions
    regarding the current time. Input is an empty string and
    the current time is returned in a string format. Only use this function
    for the current time. Other time related questions should use another tool
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


if __name__ == '__main__':
    print(get_current_time.invoke(""))
