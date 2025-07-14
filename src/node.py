from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from langchain_openai import ChatOpenAI

from src.schema import AgentState
from src.tools import update, save

load_dotenv()
tools = [update, save]
model = ChatOpenAI(model="gpt-4o").bind_tools(tools)

document_content = ""

def drafter_agent_node(state: AgentState) -> AgentState:
    system_prompt = SystemMessage(content=f"""
    You are a drafter, a helpful writing assistant. You are going to help user to update and modify the document.
    
    - If the user wants to update or modify content, use the 'update' tool with the complete updated content'
    - If the user wants to save and finish, use the 'save' tool with the complete saved content'
    - Make sure to always show the current document state after modification
    
    The current document content is: {document_content}
    
""")
    if not state["messages"]:
        user_input = "I am ready to help you update a document. what would you like to update"
        user_message = HumanMessage(content=user_input)
    else:
        user_input = input("\n what would you like to do with the document?")
        print(f"\n User: {user_input}")
        user_message = HumanMessage(content=user_input)
    all_messages = [system_prompt] + list(state["messages"]) + [user_message]
    response = model.invoke(all_messages)

    print(f"\nAI: {response.content}")
    if hasattr(response, "tool_calls") and response.tool_calls:
        print(f"\nUsing tools: {[tc['name'] for tc in response.tool_calls]}")

    return {"messages": list(state["messages"]) + [user_message, response]}

def should_continue(state: AgentState) -> str:
    """
    determine if we should continue or end the conversation
    """
    messages = state["messages"]

    if not messages:
        return "continue"
    #this looks for most recent tool messages
    for message in reversed(messages):
        if (isinstance(message, ToolMessage) and
            "saved" in message.content.lower() and
            "document" in message.content.lower()):
            return "end"
    return "continue"
