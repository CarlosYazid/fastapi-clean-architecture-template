from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from api.v1 import v1Router
from core.settings import get_settings
from core.container import Container


class AppCreator:
    def __init__(self):
        # set app default
        self.app = FastAPI(
            title=get_settings().PROJECT_NAME,
            openapi_url=f"{get_settings().API}/openapi.json",
            version="0.0.1",
        )
        
        add_pagination(self.app)

        # set db and container
        self.container = Container()
        self.db = self.container.db()
        # self.db.create_database()

        # set cors
        if get_settings().BACKEND_CORS_ORIGINS:
            self.app.add_middleware(
                CORSMiddleware,
                allow_origins=[
                    str(origin) for origin in get_settings().BACKEND_CORS_ORIGINS
                ],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )

        # set routes
        @self.app.get("/")
        def root():
            return "service is working"

        self.app.include_router(v1Router, prefix=get_settings().API_V1_STR)


app_creator = AppCreator()
app = app_creator.app
db = app_creator.db
container = app_creator.container
