import os
from fastapi import FastAPI, APIRouter
from mangum import Mangum
from fastapi.staticfiles import StaticFiles

router = APIRouter()
@router.get("/hello")
def read_root():
    return {"Hello": "World"}

app = FastAPI()
app.include_router(router, prefix="/api/v1")
SCRIPT_DIR = os.path.realpath(os.path.dirname(__file__))
app.mount("/", StaticFiles(directory=f"{SCRIPT_DIR}/front", html=True), name="front")

handler = Mangum(app)