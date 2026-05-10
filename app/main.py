from fastapi import FastAPI
from app.api.users import router as api_router

app = FastAPI(
    title="AutoLog Project API",
    description="API для керування сервісом автомобілів (Лабораторна робота №4)",
    version="2.0.0"
)

app.include_router(api_router)

@app.get("/", tags=["Root"])
async def root():
    return {"message": "AutoLog System is Online! SixSeven67"}