import sys
import os

from langgraph.graph import StateGraph
from langchain_core.documents import Document


from app.agent.knowledge_base import *
from app.agent.utils import setup_llm_client

# Add the project's root directory to the Python path
def install_if_missing(package):
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        print(f"{package} not found, installing...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", package])

class AgentInfo:
    def __init__(self, client, model_name, api_provider):
        self.client = client
        self.model_name = model_name
        self.api_provider = api_provider
        self.knowledge_store = {}

    def add_knowledge(self, key, artifacts: str):
        knowledge = create_knowledge_base(artifacts)
        self.knowledge_store[key] = knowledge

    def get_knowledge(self, key):
        return self.knowledge_store.get(key)



class RAGAgent:
    def __init__(self, knowledge_base, agent, model_name="gpt-4.1"):
        # Robust project root detection: always points to workspace root
        # This assumes this file is in <workspace>/app/agent.py
        install_if_missing('langgraph')
        install_if_missing('langchain')
        install_if_missing('langchain_community')
        install_if_missing('langchain_openai')
        install_if_missing('faiss-cpu')
        install_if_missing('pypdf')
        install_if_missing('langchain')
        install_if_missing('tavily')

        client, model_name, api_provider = setup_llm_client(model_name=model_name)
        self.agentInfo = AgentInfo(client, model_name, api_provider)

        # TODO: Update this based on project needs

        for i in range(len(knowledge_base)):
            self.agentInfo.add_knowledge(knowledge_base[i][0], knowledge_base[i][1])

        self.graph = agent

    def query(self, question, key="answer"):
        
        result = self.graph.invoke({"question": question, "documents": [], "answer": "", "agent": self.agentInfo})
        if (result and result[key]):
            return result[key]
        else:
            return ""
    
    def dict_query(self, query_dict: any, key="answer"):
        result = self.graph.invoke(query_dict)
        if (result and result[key]):
            return result[key]
        else:
            return ""


if __name__ == "__main__":
    from demo_agent import create_pm_agent, get_pm_knowledge
    # Example usage:
    # question = "What is the purpose of this project?"
    question = "What is the user class composed of?"
    # question = "How old am I?"

    agent = RAGAgent(get_pm_knowledge(), create_pm_agent(), model = "gpt-4.1")
    answer = agent.query(question)

    if answer and len(answer) > 0:
        print("Answer:", answer)
    else:
        print("No answer could be generated.")
