from typing import TypedDict, List, Any
from langgraph.graph import StateGraph
from langchain_core.documents import Document
from langgraph.graph import START, END
import json

from app.agent.utils import get_completion, setup_llm_client
from app.agent.rag_agent import AgentInfo, RAGAgent
from app.agent.knowledge_base import ExtendedKnowledgeAgent, init_knowledge

schema_artifacts = ["artifacts/schema.sql", "artifacts/seed_data.sql"]

base_knowledge = [
    ("code_schema", schema_artifacts),
]

def get_recipe_knowledge():
    return base_knowledge

class RecipeAgentState(TypedDict):
    cook_agent: ExtendedKnowledgeAgent
    coding_agent: AgentInfo
    ingredients: str
    num_recipes: int
    code_files: List[Any]
    answer: str
    recipe_list: List[dict]

def load_cook_agent_node(state: RecipeAgentState) -> RecipeAgentState:
    # role_prompt = f"""You are a professional chef that suggests recipes based on web search results and a provided list of ingredients.
    # Assist the user with their queries.
    # """
    # num_recipes = state.get("num_recipes", 3)
    # agent = ExtendedKnowledgeAgent(role=role_prompt, model="gpt-4.1", num_results=num_recipes+2)
    # return {**state, "cook_agent": agent}
    pass

def fetch_recipes_node(state: RecipeAgentState) -> RecipeAgentState:
    cook_agent = state["cook_agent"]
    ingredients = state.get("ingredients", "")
    num_recipes = state.get("num_recipes", 3)

    question = f"""
        Find the {num_recipes} best recipes to make with the ingredients below.
        Output the recipes as a valid JSON array containing each recipe
        Ensure each recipe contains the following keys:
        - 'title' - The title of the recipe
        - 'instructions' - The instructions for the recipe
        - 'description' - A brief but detailed description of the recipe
        - 'ingredients' - A list of ingredients for the recipe
        - Ingredients should also have the following keys:
            - 'name' - The name of the ingredient
            - 'quantity' - The quantity of the ingredient

        Ingredients:{ingredients}
    """
    json_output_str = cook_agent.query(question)
    if '```' in json_output_str:
        answer = json_output_str.split('```')[1].lstrip('json').strip()
    else:
        answer = json_output_str
    return {**state, "answer": answer}

def load_code_files_node(state: RecipeAgentState) -> RecipeAgentState:
    agentInfo = state["coding_agent"]
    retriever = agentInfo.get_knowledge("code_schema")
    if retriever:
        docs = retriever.invoke("We are helping the user to build a recipe from ingredients. Provide any relevant code files that might help.")
        return {**state, "code_files": docs}
    else:
        print("No code schema knowledge base found.")
        return {**state, "code_files": []}

def extract_single_recipe(agentInfo: AgentInfo, recipe_str: str, index) -> dict:
    # # schema = agentInfo.get_knowledge("code_schema")
    prompt = f"""Acting as a Senior Software Developer, extract the JSON Object at index {index} from the below JSON Array.
    Output only the valid JSON object as with no additional text.

    JSON Array: {recipe_str}
    """
    answer = get_completion(prompt, agentInfo.client, agentInfo.model_name, agentInfo.api_provider)
    try:
        recipe = json.loads(answer)
        if isinstance(recipe, dict):
            return recipe
        else:
            print(f"Extracted recipe is not a dictionary: {recipe}")
            return None
    except:
        return None

        


def extract_recipes_node(state: RecipeAgentState) -> RecipeAgentState:
    answer = state.get("answer", "")
    num_recipes = state.get("num_recipes", 3)
    agentInfo = state.get("coding_agent", {})
    recipe_list = []

    # Attempt to parse the answer as JSON after verifying with llm
    for i in range (0, num_recipes):
        recipe = extract_single_recipe(agentInfo, answer, i)
        if recipe:
            print(f"Extracted recipe {i+1}: {recipe}")
            recipe_list.append(recipe)

    return {**state, "recipe_list": recipe_list}

def create_recipe_agent():
    agent_graph = StateGraph(RecipeAgentState)
    # agent_graph.add_node("FETCH_RECIPES", load_cook_agent_node)
    agent_graph.add_node("FETCH_RECIPES", fetch_recipes_node)
    # agent_graph.add_node("LOAD_CODE_FILES", load_code_files_node)
    agent_graph.add_node("EXTRACT_RECIPES", extract_recipes_node)


    agent_graph.add_edge(START, "FETCH_RECIPES",)
    # agent_graph.add_edge("LOAD_COOK_AGENT", "FETCH_RECIPES")
    agent_graph.add_edge("FETCH_RECIPES", "EXTRACT_RECIPES")
    # agent_graph.add_edge("LOAD_CODE_FILES", "EXTRACT_RECIPES")
    agent_graph.add_edge("EXTRACT_RECIPES", END)

    rag_agent = agent_graph.compile()
    return rag_agent

class RecipeRAGAgent:
    def __init__(self, model_name="gpt-4.1"):
        ingredients = "apples, banannas, mangos"

        self.agent = RAGAgent(get_recipe_knowledge(), create_recipe_agent(), model_name = "gpt-4.1")
        num_recipes = 3

        role_prompt = f"""You are a professional chef that suggests recipes based on web search results and a provided list of ingredients.
        Assist the user with their queries.
        """
        cook_agent = ExtendedKnowledgeAgent(role=role_prompt, model="gpt-4.1", num_results=num_recipes+2)

        self.initial_recipe_state = RecipeAgentState(
            cook_agent=cook_agent,
            coding_agent=self.agent.agentInfo,
            ingredients=ingredients,
            num_recipes=num_recipes,
            code_files=[],
            answer="",
            recipe_list=[]
        )
    def query(self, ingredients:str, num_recipes:int=3) -> List[dict]:
        recipe_state = self.initial_recipe_state
        recipe_state["ingredients"] = ingredients
        recipe_state["num_recipes"] = num_recipes
        return self.agent.dict_query(recipe_state, key="recipe_list")




if __name__ == "__main__":
    # Example usage:
    recipe_agent = RecipeRAGAgent()
    ingredients = "chicken, rice, broccoli"
    answer = recipe_agent.query(ingredients)

    if answer:
        print(answer)
    else :
        print("No answer found.")

    
