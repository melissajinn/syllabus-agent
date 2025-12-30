from typing import TypedDict, List, Annotated
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages

from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage, AIMessage
from langgraph.graph import START, StateGraph, END
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from langchain_core.messages import ToolMessage
from langgraph.prebuilt import tools_condition
from pdf_load import loadpdf
from coursewebsite import loadwebsite

SYSTEM_PROMPT = """
You are a syllabus assistant.

Rules:

if data is missing and user asks question, ask them to enter something with pdf <path> or web <url>

If the user says "load <path>" and it looks like a local file path, call pdfsyllabus(path).
If the user says "load <url>" and it starts with http:// or https://, call coursewebsite(url).

if data exists, answer using content. 

- Answer ONLY using the syllabus text provided.
- If the answer is not in the syllabus, say: "I couldn't find that in the syllabus."
- Include a short quote from the syllabus as evidence when possible.
"""

class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    data: str | None
    content: str | None

def pdfsyllabus(path: str) -> str:
    """Load syllabus PDF from a local path and return extracted text."""
    return loadpdf(path)

def websyllabus(url: str) -> str:
    """Load text from a website url and return extracted text."""
    return loadwebsite(url)

# tools = [pdfsyllabus, websyllabus]

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def assistant(state: State) -> State:
    messages = state["messages"]
    system = SYSTEM_PROMPT

    if state.get("data"):
        system += "Data Type: " + state["data"]
    
    if state.get("content"):
        system += "Content Info: " + state["content"]

    reply = llm.invoke([SystemMessage(content=system)] + state["messages"])
    return {"messages": [reply]}


def webNode(state: State) -> State:
    url = state["messages"][-1].content[len("web "):].strip()
    content = websyllabus(url)
    return {
        "data": "web",
        "content": content,
        "messages": [AIMessage(content="Loaded website.")],
    }

def pdfNode(state: State) -> State:
    pdf = state["messages"][-1].content[len("pdf "):].strip()
    content = pdfsyllabus(pdf)
    return {
        "data": "pdf",
        "content": content,
        "messages": [AIMessage(content="Loaded syllabus.")],
    }

def classifier(state: State):
    text = state["messages"][-1].content.strip().lower()
    if text.startswith("pdf "):
        return "pdfNode"
    elif text.startswith("web "):
        return "webNode"
    return "assistant"

def build_app():
    graph = StateGraph(State)
    graph.add_node("assistant", assistant)
    graph.add_node("webNode", webNode)
    graph.add_node("pdfNode", pdfNode)

    graph.add_conditional_edges(START, classifier, {"pdfNode": "pdfNode", "webNode": "webNode", "assistant": "assistant"})
    graph.add_edge("pdfNode", END)
    graph.add_edge("webNode", END)

    return graph.compile()

def main():

    app = build_app()
    messages: List[AnyMessage] = []
    state = {"messages": messages, "data": None, "content": None}

    print("Syllabus Agent running. Type 'exit' to quit.")

    while True:
        user = input("\nPlease enter a question, type pdf <path> for PDF Path, type web <url> for Course Website, or type exit/quit: ").strip()
        if user.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        state["messages"].append(HumanMessage(content=user))
        state = app.invoke(state)
        messages = state["messages"]

        print("\nAgent:", messages[-1].content)


if __name__ == "__main__":
    main()
