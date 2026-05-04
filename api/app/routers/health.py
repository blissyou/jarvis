from fastapi import APIRouter

from api.app.services.model_router import router as model_router

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "jarvis-api"}


@router.get("/models/health")
def models_health() -> dict[str, object]:
    providers = [provider.__dict__ for provider in model_router.health()]
    available = [provider for provider in providers if provider["available"]]
    return {"status": "ok" if available else "degraded", "providers": providers}
