from typing import Any, Callable, List, Optional, Sequence
from fastapi.middleware.cors import CORSMiddleware
from env_config import settings
from fastapi import FastAPI

class FastAPIStarter:
    @classmethod
    def start_up(
        cls,
        title: str = settings.PROJECT_NAME,
        routers: Optional[List] = None,
        middlewares: Optional[List] = None,
        on_startup: Optional[Sequence[Callable[[], Any]]] = None,
        on_shutdown: Optional[Sequence[Callable[[], Any]]] = None,
    ) -> FastAPI:

        swagger_url = f"/docs/"

        api = FastAPI(
            title=title,
            docs_url=swagger_url,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
        )
        if settings.back_end_cors_origins:
            api.add_middleware(
                CORSMiddleware,
                allow_origins=["*"],
                allow_methods=["*"],
                allow_headers=["*"],
                allow_credentials=True,
            )

        if middlewares:
            for middleware in middlewares[::-1]:
                api.add_middleware(middleware)

        if routers:
            for route in routers[::-1]:
                api.include_router(route)


        return api
