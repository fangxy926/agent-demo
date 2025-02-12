from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor

from langchain_core.callbacks import StreamingStdOutCallbackHandler
from langchain_openai import ChatOpenAI
from tools.math import math_calculator
from tools.time import get_current_time
from tools.web_search import tavily_search

from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

llm = ChatOpenAI(temperature=0,
                 model="deepseek-v3",
                 # 配置流式输出
                 streaming=True,
                 callbacks=[StreamingStdOutCallbackHandler()])

tools = [tavily_search, math_calculator, get_current_time]

prompt = hub.pull("hwchase17/react")

agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=False,  # 配置了流式输出就不要这个了
    handle_parsing_errors=True
)

response = agent_executor.invoke({
    # "input": "温州的天气怎么样？"
    "input": "现任英国首相是谁？他上任的时候多少岁？现任首相的年龄的3次方是多少？"
})

print("\n---\n" + response["output"])
