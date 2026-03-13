from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from llm.classifier import is_database_question
from llm.generator import generate_sql
from llm.interpreter import interpret_result
from database.executor import run_query
from database.validator import validate_sql
from llm.context_resolver import resolve_context
from core.logger import get_logger

logger = get_logger(__name__)


class GraphState(TypedDict):
    question: str
    resolved_question: str
    sql: str
    is_database_question: bool
    is_write_operation: bool
    is_sql_valid: bool
    validation_message: str
    result: list
    answer: str
    history: list


def node_resolve_context(state: GraphState) -> GraphState:
    resolved = resolve_context(state["question"], state["history"])
    logger.debug(f"Resolved question: {resolved}")
    return {"resolved_question": resolved}


def node_classify(state: GraphState) -> GraphState:
    result = is_database_question(state["resolved_question"])
    logger.debug(f"Classification: {result} | Question: {state['resolved_question']}")
    return {
        "is_database_question": result == "YES",
        "is_write_operation": result == "WRITE"
    }


def node_generate_sql(state: GraphState) -> GraphState:
    sql = generate_sql(state["resolved_question"])
    logger.debug(f"Generate SQL: {sql}")
    return {"sql": sql}


def node_validate(state: GraphState) -> GraphState:
    is_valid, message = validate_sql(state["sql"])
    logger.debug(f"SQL valid: {is_valid} | Message: {message}")
    return {"is_sql_valid": is_valid, "validation_message": message}


def node_execute(state: GraphState) -> GraphState:
    logger.debug(f"Executing SQL: {state['sql']}")
    try:
        result = run_query(state["sql"])
        logger.debug(f"SQL result: {result}")
        return {"result": result}
    except Exception as e:
        logger.error(f"SQL execution error: {str(e)}")
        return {"result": [], "answer": f"Database execution error: {str(e)}"}


def node_interpret(state: GraphState) -> GraphState:
    answer = interpret_result(
        state["resolved_question"],
        state["sql"],
        state["result"],
        state["history"]
    )
    logger.debug(f"Interpreted answer: {answer}")
    return {"answer": answer}


def node_reject_off_topic(state: GraphState) -> GraphState:
    logger.debug(f"Off-topic question rejected: {state['resolved_question']}")
    return {
        "answer": "I can only answer questions about the store database. Try asking about customers, products or sales.",
        "sql": "",
        "result": []
    }


def node_reject_write_operation(state: GraphState) -> GraphState:
    logger.debug(f"Write operation rejected: {state['resolved_question']}")
    return {
        "answer": "This application currently supports read-only queries. INSERT, UPDATE and DELETE operations are not available in this version.",
        "sql": "",
        "result": []
    }


def node_reject_invalid_sql(state: GraphState) -> GraphState:
    logger.warning(f"Invalid SQL rejected: {state['sql']} | Reason: {state['validation_message']}")
    return {
        "answer": "I could not generate a valid query for that question. Please try rephrasing.",
        "sql": "",
        "result": []
    }


def node_update_history(state: GraphState) -> GraphState:
    updated_history = state.get("history", []) + [
        {"role": "user", "content": state["resolved_question"]},
        {"role": "assistant", "content": state["answer"]}
    ]
    logger.debug(f"History updated. Total messages: {len(updated_history)}")
    return {"history": updated_history}


def route_after_classify(state: GraphState) -> str:
    if state["is_write_operation"]:
        return "reject_write_operation"
    return "generate_sql" if state["is_database_question"] else "reject_off_topic"


def route_after_validate(state: GraphState) -> str:
    return "execute" if state["is_sql_valid"] else "reject_invalid_sql"


def build_graph():
    graph = StateGraph(GraphState)

    graph.add_node("resolve_context", node_resolve_context)
    graph.add_node("classify", node_classify)
    graph.add_node("generate_sql", node_generate_sql)
    graph.add_node("validate", node_validate)
    graph.add_node("execute", node_execute)
    graph.add_node("interpret", node_interpret)
    graph.add_node("reject_off_topic", node_reject_off_topic)
    graph.add_node("reject_write_operation", node_reject_write_operation)
    graph.add_node("reject_invalid_sql", node_reject_invalid_sql)
    graph.add_node("update_history", node_update_history)

    graph.add_edge(START, "resolve_context")
    graph.add_edge("resolve_context", "classify")
    graph.add_conditional_edges("classify", route_after_classify)
    graph.add_edge("generate_sql", "validate")
    graph.add_conditional_edges("validate", route_after_validate)
    graph.add_edge("execute", "interpret")
    graph.add_edge("interpret", "update_history")
    graph.add_edge("update_history", END)
    graph.add_edge("reject_off_topic", "update_history")
    graph.add_edge("reject_write_operation", "update_history")
    graph.add_edge("reject_invalid_sql", "update_history")

    memory = MemorySaver()
    return graph.compile(checkpointer=memory)


app_graph = build_graph()