import os
from fastapi import FastAPI
from mangum import Mangum
from fastapi.staticfiles import StaticFiles

app = FastAPI()

@app.get("/hello")
def read_root():
    return {"Hello": "World"}

SCRIPT_DIR = os.path.realpath(os.path.dirname(__file__))
app.mount("/", StaticFiles(directory=f"{SCRIPT_DIR}/front", html=True), name="front")

handler = Mangum(app)