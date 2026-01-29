# Routers package
from .pages import router as pages_router
from .auth import router as auth_router
from .users import router as users_router
from .prompts import router as prompts_router
from .content import router as content_router
from .collections import router as collections_router

__all__ = [
    "pages_router",
    "auth_router", 
    "users_router",
    "prompts_router",
    "content_router",
    "collections_router"
]
