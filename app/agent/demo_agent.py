from typing import TypedDict, List, Any
from langgraph.graph import StateGraph
from langchain_core.documents import Document
from langgraph.graph import START, END

from rag_agent import RAGAgent, AgentInfo
from utils import get_completion

prd_artifacts = ["artifacts/day1_prd.md"]
tech_artifacts = ["artifacts/schema.sql", "artifacts/adr_001_database_choice.md"]

base_knowledge = [
    ("prd", prd_artifacts),
    ("tech", tech_artifacts)
]

def get_pm_knowledge():
    return base_knowledge

class ProjectMgrAgentState(TypedDict):
    question: str
    documents: List[Any]
    answer: str
    researcher: str
    agent: AgentInfo

def pm_node(state: ProjectMgrAgentState) -> ProjectMgrAgentState:
    prompt = f"""
    Acting as a Project Manager, Determine who should answer the question based on the instructions provided and the question below.

    Instructions:
    Answer with only 'Software Architect', 'Product Owner', or 'no'.
    - If this is a technical question, please respond with 'Software Architect'.
    - If this is a product or project related question (non-technical), please respond with 'Product Owner'.
    - If neither would be suitable to answer the question is not sufficient to answer the question, please respond with 'no'.

    Question:
    {state['question']}
    """
    agent = state["agent"]
    researcher = get_completion(prompt, agent.client, agent.model_name, agent.api_provider).strip().lower()
    return {**state, "researcher": researcher}

def pm_router(state: ProjectMgrAgentState):
    if "software" in state.get("researcher", "").lower():
        return "tech_professional"
    elif "product" in state.get("researcher", "").lower():
        return "product_professional"
    else:
        print ("Information is not sufficient to answer question.")
        return "end"

def retrieve_docs(retriever, question: str) -> List[Document]:
    return retriever.invoke(question)
    
def prd_retrieve_node(state: ProjectMgrAgentState) -> ProjectMgrAgentState:
    retriever = state['agent'].get_knowledge("prd")
    docs = retrieve_docs(retriever, state["question"])
    return {**state, "documents": docs}

def tech_retrieve_node(state: ProjectMgrAgentState) -> ProjectMgrAgentState:
    retriever = state['agent'].get_knowledge("tech")
    docs = retrieve_docs(retriever, state["question"])
    return {**state, "documents": docs}

def ask_the_docs(agentInfo, role:str, question:str, documents:List[Document]) -> str:
    context = "\n\n".join(doc.page_content for doc in documents)
    prompt = f"""
    Acting as a Senior {role}, answer the following question using only the provided documents.
    If the documents do not have enough information, please say so before responding.
    Provide your answer only with no additional text.

    Question:
    {question}

    Documents:
    {context}

    Answer:
    """
    # response = client.chat.completions.create(
    #     model=model_name,
    #     messages=[{"role": "user", "content": prompt}],
    #     max_tokens=512
    # )
    answer = get_completion(prompt, agentInfo.client, agentInfo.model_name, agentInfo.api_provider)
    return answer

def research_node(state: ProjectMgrAgentState) -> ProjectMgrAgentState:
    doc_info = ask_the_docs(state['agent'], state['researcher'], state['question'], state['documents'])
    return {**state, "answer": doc_info}

def synthesize_node(state: ProjectMgrAgentState) -> ProjectMgrAgentState:
    prompt = f"""
    Acting as a professional Copywriter, take the following response from a {state["researcher"]} and rephrase it in a clear and engaging format.
    Please ensure that the final output is concise and retains the original meaning and contains no additional commentary.

    Response: {state["answer"]}
    """
    agent = state["agent"]
    copywritten_answer = get_completion(prompt, agent.client, agent.model_name, agent.api_provider)
    return {**state, "answer": copywritten_answer}

def create_pm_agent():
    agent_graph = StateGraph(ProjectMgrAgentState)
    agent_graph.add_node("PROJECT_MANAGER", pm_node)
    agent_graph.add_node("PRD_RETRIEVER", prd_retrieve_node)
    # agent_graph.add_node("PRD_RESEARCHER", prd_research_node)
    agent_graph.add_node("TECH_RETRIEVER", tech_retrieve_node)
    agent_graph.add_node("RESEARCHER", research_node)
    agent_graph.add_node("SYNTHESIZER", synthesize_node)

    agent_graph.add_edge(START, "PROJECT_MANAGER")
    agent_graph.add_conditional_edges("PROJECT_MANAGER", pm_router, {"tech_professional":"TECH_RETRIEVER", "product_professional":"PRD_RETRIEVER", "end":END})
    agent_graph.add_edge("PRD_RETRIEVER", "RESEARCHER")
    agent_graph.add_edge("TECH_RETRIEVER", "RESEARCHER")
    agent_graph.add_edge("RESEARCHER", "SYNTHESIZER")
    # agent_graph.add_edge("TECH_RESEARCHER", "SYNTHESIZER")
    agent_graph.add_edge("SYNTHESIZER", END)

    rag_agent = agent_graph.compile()
    return rag_agent
