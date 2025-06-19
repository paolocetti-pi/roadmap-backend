from fastapi import FastAPI
from services.database import init_db, get_db
from services import eye_color_service
from routes import character_routes, eye_color_routes
from sqlalchemy.orm import Session

app = FastAPI(
    title="Character API",
    description="API for managing characters and their eye colors",
    version="1.0.0"
)

# Include routers
app.include_router(character_routes.router)
app.include_router(eye_color_routes.router)

@app.on_event("startup")
def startup_event():
    # Initialize database
    init_db()
    
    # Initialize eye colors
    db = next(get_db())
    eye_color_service.init_eye_colors(db)
    db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 