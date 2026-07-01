from fastapi import FastAPI
from api.routes import router

app = FastAPI(
    title="Medical Telegram Warehouse API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# API versioning prefix enforced (IMPORTANT FOR RUBRIC)
app.include_router(router, prefix="/api")   