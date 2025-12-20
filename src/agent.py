from __future__ import annotations

from typing import TypedDict, List

from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.messages import AnyMessage, HumanMessage
from langgraph.graph import StateGraph, END


class State(TypedDict):
    messages: List[AnyMessage]


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


def assistant_node(state: State) -> State:
    # LLM reads all messages and replies once
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

    print("LangGraph skeleton running. Type 'exit' to quit.")
    while True:
        user = input("\nYou: ").strip()
        if user.lower() in {"exit", "quit"}:
            break

        messages.append(HumanMessage(content=user))
        result = app.invoke({"messages": messages})
        messages = result["messages"]

        print("\nAgent:", messages[-1].content)


if __name__ == "__main__":
    main()
