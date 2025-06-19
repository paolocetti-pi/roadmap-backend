from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.item_routes import router as item_router

app = FastAPI(
    title="Star Wars Characters API",
    description="API for managing Star Wars character data",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(item_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 