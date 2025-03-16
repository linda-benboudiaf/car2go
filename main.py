from fastapi import FastAPI
from database import engine, Base
from routes import user, car, booking, auth

app = FastAPI()

@app.on_event("startup")
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def home():
    return {"message": "Bienvenue sur Car2Go 🚗"}

app.include_router(user.router)
app.include_router(car.router)
app.include_router(booking.router)
app.include_router(auth.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)