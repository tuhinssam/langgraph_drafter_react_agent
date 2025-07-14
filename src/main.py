from src.graph import app
from src.utils import print_message

def run_drafter_agent():
    print("\n=====DRAFTER AGENT=====")
    state = {"messages":[]}
    for step in app.stream(state, stream_mode = "values"):
        if "messages" in step:
            print_message(step["messages"])
    print("\n=====DRAFTER AGENT FINISHED=====")

if __name__ == "__main__":
    run_drafter_agent()