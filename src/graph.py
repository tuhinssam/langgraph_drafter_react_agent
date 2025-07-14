from langgraph.constants import END
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode

from src.node import drafter_agent_node, should_continue, agent_tools
from src.schema import AgentState

graph = StateGraph(AgentState)
graph.add_node("drafter_agent_node", drafter_agent_node)
graph.add_node("tools_node", ToolNode(tools=agent_tools))

graph.set_entry_point("drafter_agent_node")
graph.add_edge("drafter_agent_node", "tools_node")

graph.add_conditional_edges("tools_node",
                            should_continue,
                            {
                                "continue": "drafter_agent_node",
                                "end": END,
                            },)
app = graph.compile()
