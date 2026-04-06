from langgraph.graph import StateGraph, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition

from prompt_library.prompt import SYSTEM_PROMPT
from utils.model_loader import ModelLoader

from tools.weather_info_tool import WeatherInfoTool
from tools.place_search_tool import PlaceSearchTool
from tools.expense_calculator_tool import CalculatorTool
from tools.currency_convertor_tool import CurrencyConverterTool

class GraphBuilder:
    def __init__(self, model_provider: str = "groq"):
        self.model_loader = ModelLoader(model_provider=model_provider)
        self.llm = self.model_loader.load_llm()
        
        self.tools = []

        # Initialize tools
        self.weather_tool = WeatherInfoTool()
        self.place_search_tool = PlaceSearchTool()
        self.calculator_tool = CalculatorTool()
        self.currency_tool = CurrencyConverterTool()
        
        # Add tools to list
        self.tools.extend([
            *self.weather_tool.weather_tool_list,
            *self.place_search_tool.place_search_tool_list,
            *self.calculator_tool.calculator_tool_list,
            *self.currency_tool.currency_converter_tool_list
        ])
        
        self.graph=None
        
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        
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

  
    
    