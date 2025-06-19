from fastapi import FastAPI
from sqlalchemy import text
from routes.character_routes import character_router
from routes.eye_color_routes import eye_color_router
from routes.keyphrase_routes import keyphrase_router
from services.database import database_service
from fastapi.middleware.cors import CORSMiddleware


class StarWarsAPI:
    """Main API class for Star Wars character management"""
    
    def __init__(self):
        self.app = FastAPI(
            title="Star Wars Characters API",
            description="API for managing Star Wars characters with OOP principles",
            version="2.0.0"
        )
        self.setup_routes()
        self.setup_events()
        
        # Initialize database
        database_service.init_db()
        
        # Add CORS middleware
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    def setup_routes(self):
        """Setup all API routes"""
        # Include routers
        self.app.include_router(character_router.get_router())
        self.app.include_router(eye_color_router.get_router())
        self.app.include_router(keyphrase_router.get_router())
        
        # Root endpoint
        @self.app.get("/")
        def root():
            return {
                "message": "Star Wars Characters API",
                "version": "2.0.0",
                "description": "API built with Object-Oriented Programming principles"
            }
    
    def setup_events(self):
        """Setup application events"""
        @self.app.on_event("startup")
        def on_startup():
            """Initialize database on startup"""
            try:
                database_service.init_db()
                print("Database initialized successfully")
            except Exception as e:
                print(f"Error initializing database: {e}")
        
        @self.app.on_event("shutdown")
        def on_shutdown():
            """Cleanup on shutdown"""
            print("Application shutting down")
    
    def get_app(self) -> FastAPI:
        """Get the FastAPI application instance"""
        return self.app


# Create API instance
api = StarWarsAPI()
app = api.get_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 