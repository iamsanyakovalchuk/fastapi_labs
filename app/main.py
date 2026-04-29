from fastapi import FastAPI
from app.api.users import router as user_router

app = FastAPI(title="User CRUD API")

app.include_router(user_router)

@app.get("/")
def root():
    return {"message": "API is working. Go to /docs for Swagger UI"}