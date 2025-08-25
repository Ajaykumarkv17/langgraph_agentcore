from typing import Annotated
from langchain.chat_models import init_chat_model
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
import os

from dotenv import load_dotenv

load_dotenv()

bedrock_api_key = os.getenv("AWS_BEARER_TOKEN_BEDROCK")
# Initialize the LLM with Bedrock
llm = init_chat_model(
    "us.amazon.nova-lite-v1:0",
    model_provider="bedrock",
    api_key=bedrock_api_key
)

# Define search tool
from langchain_community.tools import DuckDuckGoSearchRun
search = DuckDuckGoSearchRun()
tools = [search]
llm_with_tools = llm.bind_tools(tools)

# Define state
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Build the graph
graph_builder = StateGraph(State)

def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

graph_builder.add_node("chatbot", chatbot)
tool_node = ToolNode(tools=tools)
graph_builder.add_node("tools", tool_node)
graph_builder.add_conditional_edges("chatbot", tools_condition)
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")
graph = graph_builder.compile()

# Integrate with Bedrock AgentCore
from bedrock_agentcore.runtime import BedrockAgentCoreApp
app = BedrockAgentCoreApp()

@app.entrypoint
def agent_invocation(payload, context):
    tmp_msg = {"messages": [{"role": "user", "content": payload.get("prompt", "No prompt found in input")}]}
    tmp_output = graph.invoke(tmp_msg)
    return {"result": tmp_output['messages'][-1].content}

app.run()