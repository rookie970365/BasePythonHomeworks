from fastapi import APIRouter

router = APIRouter(tags=["PingPong"], prefix="/ping")


@router.get("")
def ping_pong():
    return {"message": "pong"}


@router.post("")
def create_item(description: str):
    return f"Homework_03: {description}"
