from fastapi import APIRouter, HTTPException

from prompts.audit_prompt import mitigation_prompt, risk_prompt
from prompts.categorize_prompt import build_prompt as build_categorize_prompt
from prompts.describe_prompt import build_prompt as build_describe_prompt
from prompts.estimate_prompt import build_prompt as build_estimate_prompt
from schemas.task_schema import Task
from services.ai_service import ask_llm

router = APIRouter(prefix="/ai/tasks", tags=["AI Tasks"])


@router.post("/describe")
def describe(task: Task) -> Task:
    prompt = build_describe_prompt(task)
    description = ask_llm(prompt)
    task.description = description
    return task


@router.post("/categorize")
def categorize(task: Task) -> Task:
    prompt = build_categorize_prompt(task)
    category = ask_llm(prompt)
    task.category = category
    return task


@router.post("/estimate")
def estimate(task: Task) -> Task:
    prompt = build_estimate_prompt(task)
    result = ask_llm(prompt)

    try:
        task.effort_hours = float(result)
    except (TypeError, ValueError) as exc:
        raise HTTPException(status_code=400, detail="LLM devolvió valor inválido") from exc

    return task


@router.post("/audit")
def audit(task: Task) -> Task:
    risk_analysis = ask_llm(risk_prompt(task))
    mitigation = ask_llm(mitigation_prompt(task, risk_analysis))

    task.risk_analysis = risk_analysis
    task.risk_mitigation = mitigation

    return task
