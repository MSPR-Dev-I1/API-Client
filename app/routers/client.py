from fastapi import APIRouter

router = APIRouter()


@router.get("")
async def get_client():
    """
        This API returns a simple message.
    """

    return {"Hello": "Client"}
