from typing import Annotated, TypedDict

from langgraph.graph import START, END, StateGraph

from langgraph.graph.message import add_messages

from langchain_openai import ChatOpenAI

from langgraph.prebuilt import ToolNode, tools_condition

from services.tools import get_food_info, add_new_food_to_database, get_daily_log, add_food_to_daily_log

from dotenv import load_dotenv

from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()







llm = ChatOpenAI()
tools = [get_food_info, get_daily_log, add_food_to_daily_log, add_new_food_to_database]

llm_with_tools = llm.bind_tools(tools)

class State(TypedDict):
    messages: Annotated[list, add_messages]

def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

graph_builder = StateGraph(State)


tool_node = ToolNode(tools=tools)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", tool_node)

graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)

graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")

graph = graph_builder.compile()

def get_bot_response(message, history):
    messages = []
    for human_msg, ai_msg in history:
        messages.append(HumanMessage(human_msg))
        messages.append(AIMessage(ai_msg))
    messages.append(HumanMessage(message))
    response = graph.invoke({'messages': messages})

    return response['messages'][-1].content

def test():

    def stream_graph_updates(user_input: str):
        for event in graph.stream({"messages": [("user", user_input)]}):
            for value in event.values():
                print("Assistant:", value)#["messages"][-1].content)
    #stream_graph_updates("Hello!")
    #print(graph.invoke({'messages' : [("user", 'i want to add a new food item in the database, it is an egg with 100 calories'),
    #                                  ("assistant", "I will need more information about the egg to add it to the database. Could you please provide the amount of protein, carbohydrates, fat, and fiber in the egg per serving?"),
    #                                    ("user", "sure, protein is 100, carbs are 100, fat is 2"),
    #                                    ("assistant","It seems like I missed the fiber information for the egg. Could you please provide the amount of fiber in the egg per serving as well?"),
    #                                    ("user", "sure fiber is 55")
    #                               ]}))
    #llm = ChatOpenAI().bind_tools(tools)
    #print(graph.invoke({'messages': [('user', 'hi')]})['messages'][-1].content)
    stream_graph_updates('please add a banana shake and 2 eggs to my daily log')
    #print(graph.invoke({'messages': [('user', 'i just ate 3 eggs, please add to log')]}))
    #print(llm.invoke("can you give me a plan to get 2500 calories only using banana, milk, oats, eggs and english oven multigrain bread"))

