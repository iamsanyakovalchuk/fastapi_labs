from fastapi import FastAPI
from app.api.users import router as api_router
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(
    title="AutoLog Project API",
    description="API для керування сервісом автомобілів",
    version="2.0.0"
)

# Підключаємо твій роутер
app.include_router(api_router)

# ВАЖЛИВО: Запускаємо збирач метрик прямо тут, у головному тілі файлу!
Instrumentator().instrument(app).expose(app)

@app.get("/", tags=["Root"])
async def root():
    return {"message": "AutoLog System is Online! SixSeven67"}