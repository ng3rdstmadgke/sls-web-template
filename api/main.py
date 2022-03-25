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
PROJECT_ROOT = os.path.realpath(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
app.mount("/", StaticFiles(directory=f"{PROJECT_ROOT}/front_dist", html=True), name="front")

handler = Mangum(app)