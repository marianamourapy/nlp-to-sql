from fastapi import FastAPI
from pydantic import BaseModel
from core.orchestrator import ask
from core.logger import get_logger

logger = get_logger(__name__)

app = FastAPI(
    title="NL2SQL — v1.0",
    description="Ask questions in natural language and get answers from a SQL database.",
    version="1.0.0"
)


class QuestionRequest(BaseModel):
    question: str


class AnswerResponse(BaseModel):
    question: str
    answer: str


@app.get("/")
def root():
    return {"message": "NLP to SQL API is running!"}

@app.post("/ask", response_model=AnswerResponse)
def ask_question(request: QuestionRequest):
    logger.info(f"API request: {request.question}")
    answer = ask(request.question)
    logger.info(f"API response: {answer}")
    return AnswerResponse(question=request.question, answer=answer)