from langchain.tools import tool


@tool
def math_calculator(input: str) -> str:
    """用于解决数学问题的计算器工具"""
    try:
        return str(eval(input))
    except:
        return "无法计算"


if __name__ == '__main__':
    print(math_calculator.invoke("2+2"))
