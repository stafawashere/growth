"""The Desmos fluency routes of docs/calculator/build-plan.md, Contracts, thin over
app/calculator_drills/service.py and app/progress/calculator_fluency.py.

Every route here writes calculator_drills and audit_log or nothing (invariant C0 in
docs/calculator/architecture.md); none reaches skills_state, attempts or sessions.
"""
from typing import Any, Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, StrictBool, StrictStr

from app.api.deps import current_user, get_db
from app.calculator_drills import service
from app.progress import calculator_fluency

router = APIRouter(tags=["calculator"])


class DrillRequest(BaseModel):
   capability: Literal["plot", "zero", "derivative", "integral", "intersection", "value", "mixed"]
   template_id: str | None = None


class DrillAnswer(BaseModel):
   value: StrictStr
   setup_mathjson: Any = None
   elapsed_ms: int = Field(ge=0)
   desmos_open: StrictBool


@router.get("/calculator/cards")
def read_cards(user=Depends(current_user)):
   return {"cards": service.card_summaries()}


@router.get("/calculator/cards/{card_id}")
def read_card(card_id: str, user=Depends(current_user)):
   record = service.card(card_id)

   if record is None:
      raise HTTPException(status_code=404, detail="no such card")

   return record


@router.post("/calculator/drills")
def serve_drill(body: DrillRequest, db=Depends(get_db, scope="function"), user=Depends(current_user)):
   try:
      return service.serve(db, user.id, body.capability, template_id=body.template_id)
   except service.UnknownTemplate as unknown:
      raise HTTPException(status_code=422, detail=str(unknown)) from unknown


@router.post("/calculator/drills/{drill_id}/answer")
def answer_drill(drill_id: str, body: DrillAnswer, db=Depends(get_db, scope="function"), user=Depends(current_user)):
   try:
      return service.answer(db, user.id, drill_id, body.value, body.setup_mathjson, body.elapsed_ms, body.desmos_open)
   except service.DrillNotFound as missing:
      raise HTTPException(status_code=404, detail="no such drill") from missing
   except service.DrillAlreadyAnswered as answered:
      raise HTTPException(status_code=409, detail="this drill has been answered") from answered


@router.get("/calculator/measured")
def read_measured(db=Depends(get_db, scope="function"), user=Depends(current_user)):
   return calculator_fluency.measured(db, user.id)
