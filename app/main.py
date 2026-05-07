from fastapi import FastAPI
from app.api.users import router as user_router

app = FastAPI(
    title="User CRUD API",
    description="API для керування користувачами (Лабораторна робота №3)",
    version="1.0.0"
)
app.include_router(user_router)

@app.get("/", tags=["Root"])
async def root():
    return {"message": "SixSevenSIXSEVEEEEEEEEEEEEEEEEEEEEEEN676767"}