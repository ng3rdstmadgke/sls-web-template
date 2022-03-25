import os
from fastapi import FastAPI, APIRouter
from mangum import Mangum
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request

router = APIRouter()
@router.get("/hello")
def hello():
    return {"Hello": "World"}

@router.get("/event")
def event(request: Request):
    print(request.scope["aws.context"])
    return {
        "event": request.scope["aws.event"],
    }

app = FastAPI()
app.include_router(router, prefix="/api/v1")
PROJECT_ROOT = os.path.realpath(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
app.mount("/", StaticFiles(directory=f"{PROJECT_ROOT}/front_dist", html=True), name="front")

handler = Mangum(app)