from langchain_core.messages import ToolMessage


def print_message(messages):
    """
    print the message in more readable format
    """
    for msg in messages[-3:]:
        if isinstance(msg, ToolMessage):
            print(f"Tool Result: {msg.content}")