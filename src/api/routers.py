from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter()

@router.get("/")
async def redirect_to_api():
    return RedirectResponse("/api/v1")

@router.get("/api/v1")
async def hello_world():
    return {"Message:", "HelloWorld!"}
