from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor
import os
from langchain_core.callbacks import StreamingStdOutCallbackHandler
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_ollama import OllamaLLM
from langchain_openai import ChatOpenAI
from tools.math import math_calculator
from tools.time import get_current_time
from tools.web_search import tavily_search, serpapi_search
from langchain.prompts import load_prompt

from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

# 调用类OpenAI接口
llm = ChatOpenAI(temperature=0.6,
                 model="deepseek-v3",
                 # model="gpt-3.5-turbo",
                 # 配置流式输出
                 streaming=True,
                 callbacks=[StreamingStdOutCallbackHandler()])

# # 调用Ollama的模型
# llm = OllamaLLM(
#     base_url=os.getenv('OLLAMA_BASE_URL'),
#     temperature=0.6,
#     model="qwen2.5:1.5b",
#     # 配置流式输出
#     streaming=True,
#     callbacks=[StreamingStdOutCallbackHandler()]
# )

tools = [tavily_search, math_calculator, get_current_time]

# 方式1：从hub上直接拉取别人写好的prompt
# prompt = hub.pull("hwchase17/react")
# print(prompt.template)

#
# # 方式2：自己写prompt
# system_prompt = """
# Answer the following questions as best you can. You have access to the following tools:
#
# {tools}
#
# Use the following format:
#
# Question: the input question you must answer
# Thought: you should always think about what to do
# Action: the action to take, should be one of [{tool_names}]
# Action Input: the input to the action
# Observation: the result of the action
# ... (this Thought/Action/Action Input/Observation can repeat N times)
# Thought: I now know the final answer
# Final Answer: the final answer to the original input question
#
# Begin!
#
# Question: {input}
# Thought:{agent_scratchpad}
# """
# prompt = PromptTemplate.from_template(system_prompt)

# 方式3：自己写prompt（文件中加载）
prompt = load_prompt("prompt/react_prompt.json")
# print(prompt.template)

agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=False,  # 配置了流式输出就不要这个了
    handle_parsing_errors=True
)

response = agent_executor.invoke({
    # "input": "现任美国总统是谁？他上任了多少年？上任时长（按年算）的3次方是多少？",
    "input": "今天是几号？温州的天气如何？"
})

print("\n---\n" + response["output"])

## 写在最后：实验证明deepseek-v3的function call还存在问题，qwen2.5和gpt-3.5都正常
