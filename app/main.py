from fastapi import FastAPI
from .database import engine
from .models import Base
from .routers import post, user, auth
from .config import settings

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
