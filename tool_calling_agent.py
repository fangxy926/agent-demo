from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor, create_tool_calling_agent
import os
from langchain_core.callbacks import StreamingStdOutCallbackHandler
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from langchain_openai import ChatOpenAI
from tools.math import math_calculator
from tools.time import get_current_time
from tools.web_search import tavily_search, serpapi_search

from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

# 调用类OpenAI接口
llm = ChatOpenAI(temperature=0.6,
                 # model="gpt-3.5-turbo",
                 model="deepseek-v3",
                 # 配置流式输出
                 streaming=True,
                 callbacks=[StreamingStdOutCallbackHandler()])

tools = [tavily_search, math_calculator, get_current_time]

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant.",
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=False,  # 配置了流式输出就不要这个了
    handle_parsing_errors=True
)

response = agent_executor.invoke({
    # "input": "现任美国总统是谁？他上任了多少年？上任时长（按年算）的3次方是多少？"
    "input": "现在的日期和时间？"
})

print("\n---\n" + response["output"])
