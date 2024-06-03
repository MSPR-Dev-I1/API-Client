from fastapi import APIRouter, HTTPException
from app.database import test_connection

router = APIRouter()


@router.get("")
async def get_client():
    """
        This API tests the connection with the database and returns a simple message.
    """
    try:
        test_connection()
        return {"Hello": "Client"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Connection failed: {e}")
