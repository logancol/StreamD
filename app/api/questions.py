from fastapi import APIRouter, Depends, HTTPException, Request
from app.db.db import get_async_conn
from psycopg import AsyncConnection
from app.services.oracle import Oracle
from app.core.config import settings
import logging

router = APIRouter()

log = logging.getLogger(__name__)

@router.get("/question")
async def get_answer(question: str, request: Request, conn: AsyncConnection = Depends(get_async_conn)) -> str:
    log.info(f"====== QUESTION ENDPOINT HIT, QUESTION: {question} ======")
    oracle = Oracle(logger=log, schema=request.app.state.schema, client=request.app.state.openai_client)
    return await oracle.ask_oracle(question, conn=conn)