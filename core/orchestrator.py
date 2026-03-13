from groq import RateLimitError
from core.graph import app_graph
from core.logger import get_logger

logger = get_logger(__name__)


def ask(question: str, thread_id: str = "default") -> str:
    config = {"configurable": {"thread_id": thread_id}}

    state = app_graph.get_state(config)
    history = state.values.get("history", []) if state.values else []

    logger.debug(f"Question {question} | Thread: {thread_id} | History length: {len(history)}")

    try:
        result = app_graph.invoke(
            {"question": question, "history": history},
            config=config
        )
        answer = result.get("answer", "I could not process your question. Please try again.")

    except RateLimitError:
        logger.warning("Groq rate limit reached.")
        answer = "The system is temporarily busy due to high usage. Please wait a few seconds and try again."

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        answer = "An unexpected error occurred. Please try again."

    logger.debug(f"Answer: {answer}")
    return answer