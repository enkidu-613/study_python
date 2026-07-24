from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.routers.auth import get_current_user
from app.services.dify_service import run_dify_workflow

router = APIRouter(prefix="/dify", tags=["dify"])


class DifyQuestion(BaseModel):
    question: str = Field(min_length=1, max_length=1000)


@router.post("/rag")
async def ask_dify(
    request: DifyQuestion, current_user: dict = Depends(get_current_user)
):
    answer = await run_dify_workflow(
        question=request.question, user_id=f"user:{current_user['id']}"
    )
    return answer
