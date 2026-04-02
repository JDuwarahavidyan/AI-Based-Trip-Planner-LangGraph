from langgraph.graph import StateGraph, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition

from prompt_library.prompt import SYSTEM_PROMPT


class GraphBuilder:
    def __init__(self):
        
        
        
        
        self.system_prompt = SYSTEM_PROMPT

    def agent_function(self, state: MessagesState):
        """Main agent function"""
        user_question = state["messages"]
        input_question = [self.system_prompt] + user_question
        response = self.llm_with_tools.invoke(input_question)
        return {"messages": [response]}		
		
    
    def build_graph(self):
        
        graph_builder=StateGraph(MessagesState)
        graph_builder.add_node("agent", self.agent_function)
        graph_builder.add_node("tools", ToolNode(tools=self.tools))
        graph_builder.set_entry_point("agent")

        graph_builder.add_conditional_edges(
            "agent",
            tools_condition
        )   # tool condition will return whether to use tools or not based on that it will go ["tools", END]
    
        graph = graph_builder.compile()
        
        return graph
    
    def __call__(self):
        return self.build_graph()    

  
    
    