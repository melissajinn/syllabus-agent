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
You are a syllabus assistant, helping with syllabus questions, homework questions, or grading homework. 

Rules:
- If the user asks about how to USE this assistant (like "how do I upload?", "how does this work?", "what can you do?"), explain that they can:
  1. Upload a PDF syllabus using the "Upload PDF" button
  2. Load a website syllabus by typing: web <url>
  3. Ask questions about the syllabus once it's loaded
  4. Type "summary" to get a summary of the loaded content
  5. upload a pdf of a completed homework assignment to grade it
  
- If no content has been loaded yet, politely ask the user to load a syllabus or homework assignment first by:
  - Clicking the "Upload PDF" button to upload a PDF syllabus/PDF homework assignment
  - Typing "web <url>" to load a website syllabus
  
- Once content is loaded:
1. If the user asks a question about the syllabus, answer using the content of the syllabus.
  - Answer ONLY using the content provided.
  - If answer not in the syllabus, say: "I couldn't find that in the syllabus."
  - Include a short quote from the syllabus as evidence when possible.
  - If user asks a question about a specific course topic, look over content and respond with info that will help them figure out the question:
    Where to look: <section / lecture number>
    Next steps: <what the student should do or check next>
    Do not immediately give answer, provide guidance on where to look in the syllabus and what to check next.

2. If the user asks for you to grade their homework, look over the content of the homework assignment
  - if it doesnt seem like a homework assignment, say "This doesn't look like a homework assignment. Please upload a PDF of your completed homework assignment."
  - provide feedback on what was done well and what could be improved.

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
    system = SYSTEM_PROMPT

    if state.get("data"):
        system += "Data Type: " + state["data"]
    
    if state.get("content"):
        system += "Content Info: " + state["content"]
    else:
        system += "\nNote: No content has been loaded yet."

    reply = llm.invoke([SystemMessage(content=system)] + state["messages"])
    return {"messages": [reply]}


def webNode(state: State) -> State:
    url = state["messages"][-1].content[len("web "):].strip()
    c = websyllabus(url)
    return {"data": "web",
            "content": c,
            "messages": [AIMessage(content="Loaded website")]}

def pdfNode(state: State) -> State:
    pdf = state["messages"][-1].content[len("pdf "):].strip()
    c = pdfsyllabus(pdf)
    DOC_TYPES = ["syllabus", "homework", "none"]

    classifierprompt = "Classify the following content as either 'syllabus', 'homework', or 'none'. Return ONLY the label. \n\nContent:" + c[:2000]
    label = llm.invoke([SystemMessage(content=classifierprompt)])
    
    return {
        "data": label.content.strip().lower(),
        "content": c,
        "messages": [AIMessage(content="Loaded Syllabus" if label == "syllabus" else "Loaded Homework")],
    }

def classifier(state: State):
    text = state["messages"][-1].content.strip().lower()
    if text.startswith("pdf "):
        return "pdf"
    elif text.startswith("web "):
        return "web"
    elif "summary" in text:
        return "summary"
    return "assistant"

def summaryNode(state: State):
    system = "provide a summarization of the content if available"
    reply = llm.invoke([SystemMessage(content=system)] + state["messages"])
    return {"messages": [reply]}


def build_app():
    graph = StateGraph(State)
    graph.add_node("assistant", assistant)
    graph.add_node("webNode", webNode)
    graph.add_node("pdfNode", pdfNode)
    graph.add_node("summaryNode", summaryNode)

    graph.add_conditional_edges(START, classifier, {"pdf": "pdfNode", "web": "webNode", "assistant": "assistant", "summary": "summaryNode"})
    graph.add_edge("pdfNode", END)
    graph.add_edge("webNode", END)
    graph.add_edge("summaryNode", END)

    return graph.compile()

def main():

    app = build_app()
    messages: List[AnyMessage] = []
    state = {"messages": messages, "data": None, "content": None}

    print("Syllabus Agent running. Type 'exit' to quit.")
    i = ""

    while True:
        if state.get("data"):
            i = "\nPlease enter a question, type pdf <path>, web <url>, summary, or exit/quit: "
        else:
            i = "\nPlease type pdf <path>, web <url>, or exit/quit: "
        user = input(i).strip()
        if user.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        state["messages"].append(HumanMessage(content=user))
        state = app.invoke(state)
        messages = state["messages"]

        print("\nAgent:", messages[-1].content)


if __name__ == "__main__":
    main()
