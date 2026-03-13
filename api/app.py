from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes.restaurants import router as restaurant_router

app = FastAPI(title="Redis Geo API")

# Allow mobile and desktop apps to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(restaurant_router, prefix="/api")

@app.get("/")
def root():
    return {"status": "online"}