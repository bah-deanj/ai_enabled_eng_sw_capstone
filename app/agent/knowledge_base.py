import sys
import os

from app.agent.utils import setup_llm_client
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

project_root = "."

def init_knowledge():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

def create_knowledge_base(file_paths):
    """Loads documents from given paths and creates a FAISS vector store.""" 
    all_docs = []
    for path in file_paths:
        full_path = os.path.join(project_root, path)
        if os.path.exists(full_path):
            loader = TextLoader(full_path)
            docs = loader.load()
            for doc in docs:
                doc.metadata={"source": path} # Add source metadata
            all_docs.extend(docs)
        else:
            print(f"Warning: Artifact not found at {full_path}")

    if not all_docs:
        print("No documents found to create knowledge base.")
        return None

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(all_docs)
    
    print(f"Creating vector store from {len(splits)} document splits...")
    vectorstore = FAISS.from_documents(documents=splits, embedding=OpenAIEmbeddings())
    return vectorstore.as_retriever()

#only supports openai for now

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
class ExtendedKnowledgeAgent:
    def __init__(self, role:str, model:str, num_results:int=5):
        client, model_name, api_provider = setup_llm_client(model_name=model)
        llm = ChatOpenAI(model=model_name)
        # 1. Instantiate the Tavily search tool
        search_tool = TavilySearchResults(max_results=num_results)
        tools = [search_tool]

        # Create the prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", role),
            ("user", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ])
        print("Prompt template created.")
        # 3. Create the agent
        agent = create_tool_calling_agent(llm, tools, prompt)

        # 4. Create the AgentExecutor
        self.agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    def query(self, question: str):
        # 5. Invoke the agent with a question
        result = self.agent_executor.invoke({"input": question})
        print(result)
        return result.get('output', result)

# python -m app.agent.knowledge_base 
if __name__ == "__main__":
    init_knowledge()
    ingredients = ["chicken", "rice", "broccoli", "soy sauce", "garlic"]
    role_prompt = f"""You are a professional chef that suggests recipes based on web search results and a provided list of ingredients.
    Assist the user with their queries.
    """
    agent = ExtendedKnowledgeAgent(role=role_prompt, model="gpt-4o", num_results=5)
    agent.query(f"""Find the 3 best recipes to make with these ingredients:
    Ingredients:{ingredients}
    """)