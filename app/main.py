from fastapi import FastAPI
from app.core.config import settings
from app.api.routes import auth as auth_routes
from app.api.routes import users as users_routes

app = FastAPI(title=settings.project_name)

@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}

app.include_router(auth_routes.router, prefix="/auth", tags=["auth"])
app.include_router(users_routes.router, prefix="/users", tags=["users"])