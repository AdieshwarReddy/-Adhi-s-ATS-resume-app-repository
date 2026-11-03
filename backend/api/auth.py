from fastapi import APIRouter

router = APIRouter()

@router.get("/me")
def get_me():
    return {"user": "current_user_placeholder"}
