from fastapi import APIRouter

from api.app.schemas.contracts import ToolManifest
from api.app.services.tools import list_tools

router = APIRouter(prefix="/tools", tags=["tools"])


@router.get("", response_model=list[ToolManifest])
def get_tools() -> list[ToolManifest]:
    return list_tools()
