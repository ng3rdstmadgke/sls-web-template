import os

from fastapi import FastAPI, Depends
from mangum import Mangum
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from api.api.db import db
from api.api.routers import item, token, user, role
from api.api.env import get_env, Mode

if get_env().mode == Mode.PRD:
    app = FastAPI(
        redoc_url=None,
        docs_url=None,
        openapi_url=None,
        root_path=os.getenv("API_GATEWAY_BASE_PATH", "")
    )
    allow_origins = []
else:
    # NOTE: dev環境ではAPI documentを表示
    app = FastAPI(
        redoc_url="/api/redoc",
        docs_url="/api/docs",
        openapi_url="/api/docs/openapi.json",
        root_path=get_env().api_gateway_base_path
    )
    allow_origins = ["*"]

# CORS: https://fastapi.tiangolo.com/tutorial/cors/
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router, prefix="/api/v1")
app.include_router(role.router, prefix="/api/v1")
app.include_router(item.router, prefix="/api/v1")
app.include_router(token.router, prefix="/api/v1")

@app.get("/api/healthcheck")
async def healthcheck(
    db: Session = Depends(db.get_db),
):
    stmt = text(f"SELECT 'healthy' as message")
    row = db.execute(stmt).first()
    return {"message": row.message}


PROJECT_ROOT = os.path.realpath(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
app.mount("/", StaticFiles(directory=f"{PROJECT_ROOT}/front_dist", html=True), name="front")

handler = Mangum(app)
