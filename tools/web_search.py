from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities import SerpAPIWrapper

from langchain.tools import tool
import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())


@tool
def tavily_search(query: str, max_results: int = 3) -> str:
    """
    使用Tavily搜索引擎进行网络搜索，返回结构化结果。

    Args:
        query (str): 搜索查询内容（建议使用英文关键词）

    Returns:
        str: 格式化的搜索结果，包含摘要和参考链接
             格式示例：
             [结果1] 内容摘要...
             参考链接：[标题](url)
             ---
             [结果2] 内容摘要...
             参考链接：[标题](url)

    Raises:
        ValueError: 当API密钥未配置时
    """
    try:
        # 初始化官方工具（建议在应用启动时初始化以提高性能）
        search_tool = TavilySearchResults(
            api_key=os.getenv("TAVILY_API_KEY"),  # 从环境变量获取
            max_results=max_results,  # 返回多少搜索结果
            search_depth="advanced"  # 深度搜索模式
        )

        # 执行搜索请求
        response = search_tool.invoke({"query": query})

        # 处理并格式化结果
        formatted_results = []
        for idx, result in enumerate(response, 1):
            content = result.get("content", "未找到相关内容").replace("\n", " ").strip()
            # todo 提取摘要
            url = result.get("url", "#")

            # 构建条目，封装成json
            entry = {
                "index": idx,
                "content": content,
                "url": url
            }
            formatted_results.append(entry)

        return formatted_results

    except Exception as e:
        return f"搜索执行失败：{str(e)}"


@tool
def serpapi_search(query: str) -> str:
    """使用 SerpAPI 执行网络搜索。"""
    params = {
        "engine": "google",
        "gl": "cn",
        "hl": "zh-cn",
    }
    search = SerpAPIWrapper(params=params)
    return search.run(query)


# 使用示例
if __name__ == "__main__":
    # 测试搜索

    print(tavily_search.invoke("温州今天天气怎么样？"))
    # print(serpapi_search.invoke("温州今天天气怎么样？"))
