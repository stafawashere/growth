"""GET /content/snapshot: the active snapshot id, digest and counts."""
import json

from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import current_user, get_db
from app.db import models

router = APIRouter(prefix="/content", tags=["content"])


@router.get("/snapshot")
def read_snapshot(db=Depends(get_db), user=Depends(current_user)):
   row = (
      db.query(models.ContentSnapshot)
      .filter(models.ContentSnapshot.status == "active")
      .order_by(models.ContentSnapshot.loaded_at.desc())
      .first()
   )
   is_missing = row is None

   if is_missing:
      raise HTTPException(status_code=404, detail="no active content snapshot")

   return {
      "id": row.id,
      "digest": row.digest,
      "loaded_at": row.loaded_at,
      "library_commit": row.library_commit,
      "counts": json.loads(row.counts),
   }
