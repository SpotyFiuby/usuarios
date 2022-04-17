from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.routers import user_controller


# For testing purposes
def create_app():
    _app = FastAPI()
    origins = ["*"]

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    _app.include_router(user_controller.router)

    @_app.get("/", tags=["Home"])
    def home():
        return {"message": "Spotifiuba - 2022"}

    return _app


app = create_app()
