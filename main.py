from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.routers import user_controller

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_controller.router)


@app.get("/", tags=["Home"])
def home():
    return "Spotifiuba - 2022"
