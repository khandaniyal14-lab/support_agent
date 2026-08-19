from fastapi import APIRouter, HTTPException

from app.ai.classifier import TicketClassifier
from app.schemas.ai import AnalyzeTicketRequest

router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


classifier = TicketClassifier()


@router.post("/analyze-ticket")
def analyze_ticket(
    request: AnalyzeTicketRequest,
):
    try:
        result = classifier.classify(
            request.ticket
        )

        return result.model_dump()

    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="AI classification failed.",
        ) from exc