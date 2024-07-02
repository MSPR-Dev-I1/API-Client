from fastapi import APIRouter


router = APIRouter()


@router.get("", tags=["client"])
async def demo():
    """
    Demo
    """
    return {"Demo": "MSPR"}
