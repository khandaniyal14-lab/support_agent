from fastapi import APIRouter
from sqlalchemy import text

from app.db.session import SessionLocal

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("")
def health_check():
    db = SessionLocal()

    try:
        db.execute(text("SELECT 1"))

        database_status = "healthy"

    except Exception:  # noqa: BLE001
        database_status = "unhealthy"

    finally:
        db.close()

    return {
        "status": "ok",
        "database": database_status,
    }