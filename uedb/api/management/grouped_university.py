from fastapi import APIRouter

router = APIRouter(prefix="/grouped_university")


@router.get("/asdf")
def asdf():
    return []
