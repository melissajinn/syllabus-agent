from typing import TypedDict, List, Literal

from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from langchain_core.messages import ToolMessage
from langgraph.prebuilt import tools_condition
from pdf_load import loadpdf
from coursewebsite import loadwebsite

SYSTEM_PROMPT = """
You are a syllabus assistant.

Rules:

if syllabus_text is missing and user asks question, ask them to enter something with pdf <path> or web <url>

If the user says "load <path>" and it looks like a local file path, call pdfsyllabus(path).
If the user says "load <url>" and it starts with http:// or https://, call coursewebsite(url).

if syllabus_text exists, answer using it. 

- Answer ONLY using the syllabus text provided.
- If the answer is not in the syllabus, say: "I couldn't find that in the syllabus."
- Include a short quote from the syllabus as evidence when possible.
"""

class State(TypedDict):
    messages: List[AnyMessage]
    syllabus_text: str | None

@tool
def pdfsyllabus(path: str) -> str:
    """Load syllabus PDF from a local path and return extracted text."""
    return loadpdf(path)

def websyllabus(url: str) -> str:
    """Load text from a website url and return extracted text."""
    return loadwebsite(url)

def store_syllabus_node(state: State) -> State:
    last = state["messages"][-1]
    if isinstance(last, ToolMessage):
        return {"messages": state["messages"][:-1], "syllabus_text": last.content}
    return state

tools = [pdfsyllabus, websyllabus]

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
llmt = llm.bind_tools(tools)

def assistant_node(state: State) -> State:
    messages = state["messages"]
    system = SYSTEM_PROMPT

    if state.get("syllabus_text"):
        system += "SYLLABUS TEXT: " + state["syllabus_text"]

    if not messages or not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=system)] + messages
    else:
        messages[0] = SystemMessage(content=system)

    if isinstance(messages[-1], ToolMessage):
        return {**state, "messages": messages}

    reply = llmt.invoke(messages)
    return {**state, "messages": messages + [reply]}

def build_app():
    graph = StateGraph(State)
    graph.add_node("assistant", assistant_node)
    graph.add_node("tools", ToolNode(tools))
    graph.add_node("store", store_syllabus_node)
    graph.set_entry_point("assistant")
    graph.add_conditional_edges("assistant", tools_condition, {"tools": "tools", END: END})
    graph.add_edge("tools", "store")
    graph.add_edge("store", "assistant")      
    return graph.compile()

def main():

    app = build_app()
    messages: List[AnyMessage] = []
    state = {"messages": messages, "syllabus_text": None}

    print("Syllabus Agent running. Type 'exit' to quit.")

    while True:
        user = input("\nPlease enter a question, type pdf <path> for PDF Path, type web <url> for Course Website, or type exit/quit: ").strip()
        if user.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        if user.startswith("pdf "):
            path = user[len("pdf "):].strip()
            state["syllabus_text"] = loadpdf(path)
            print("Loaded syllabus.")
            continue

        if user.startswith("web "):
            path = user[len("web "):].strip()
            state["syllabus_text"] = websyllabus(path)
            print(state["syllabus_text"])
            print("Loaded website.")
            continue

        state["messages"].append(HumanMessage(content=user))
        state = app.invoke(state)
        messages = state["messages"]

        print("\nAgent:", messages[-1].content)


if __name__ == "__main__":
    main()
