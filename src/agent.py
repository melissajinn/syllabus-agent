from typing import TypedDict, List

from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from pdf_load import loadpdf

class State(TypedDict):
    messages: List[AnyMessage]


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


def assistant_node(state: State) -> State:
    reply = llm.invoke(state["messages"])
    return {"messages": state["messages"] + [reply]}


def build_app():
    graph = StateGraph(State)
    graph.add_node("assistant", assistant_node)
    graph.set_entry_point("assistant")
    graph.add_edge("assistant", END)
    return graph.compile()


def main():
    app = build_app()
    messages: List[AnyMessage] = []

    print("Syllabus Agent running. Type 'exit' to quit.")
    loadpdf() #now syllabus.txt holds syllabus

    with open("/Users/melissajin/syllabus-agent/data/syllabus.txt", "r", encoding="utf-8") as f:
        syllabus_text = f.read()

    SYSTEM_PROMPT = """
    You are a syllabus assistant.

    Rules:
    - Answer ONLY using the syllabus text provided.
    - If the answer is not in the syllabus, say: "I couldn't find that in the syllabus."
    - Include a short quote from the syllabus as evidence when possible.

    Here is the syllabus:
    """ + syllabus_text

    messages = [SystemMessage(content=SYSTEM_PROMPT)] +  messages

    while True:
        user = input("\nPlease enter your question, or type exit/quit: ").strip()
        if user.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        messages.append(HumanMessage(content=user))
        result = app.invoke({"messages": messages})
        messages = result["messages"]

        print("\nAgent:", messages[-1].content)


if __name__ == "__main__":
    main()
