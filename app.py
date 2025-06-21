from fastapi import FastAPI
from sqlalchemy import text
from routes.character_routes import character_router
from routes.eye_color_routes import eye_color_router
from routes.keyphrase_routes import keyphrase_router
from routes.user_routes import router as user_router
from routes.sso_routes import router as sso_router
from services.database import database_service
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request, Response
from slowapi.middleware import SlowAPIMiddleware
from utils.logger import setup_logger
import logging


class StarWarsAPI:
    """Main API class for Star Wars character management"""
    
    def __init__(self):
        self.logger = setup_logger()
        self.app = FastAPI(
            title="Star Wars Characters API",
            description="API for managing Star Wars characters with OOP principles",
            version="2.0.0"
        )
        # Add SlowAPI middleware for rate limiting
        self.app.add_middleware(SlowAPIMiddleware)
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
        # Add security headers middleware
        @self.app.middleware("http")
        async def add_security_headers(request: Request, call_next):
            response: Response = await call_next(request)
            response.headers["Content-Security-Policy"] = "default-src 'self'; style-src 'self' https://cdn.jsdelivr.net; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; img-src 'self' https://fastapi.tiangolo.com data:;"
            response.headers["X-Frame-Options"] = "DENY"
            response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains; preload"
            response.headers["X-Content-Type-Options"] = "nosniff"
            response.headers["Referrer-Policy"] = "no-referrer"
            response.headers["X-XSS-Protection"] = "1; mode=block"
            response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
            return response
        # Add global rate limiting
        limiter = Limiter(key_func=get_remote_address, default_limits=["5/minute"])
        self.app.state.limiter = limiter
        self.app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
        self.limiter = limiter
    
    def setup_routes(self):
        """Setup all API routes"""
        # Include routers
        self.app.include_router(character_router.get_router())
        self.app.include_router(eye_color_router.get_router())
        self.app.include_router(keyphrase_router.get_router())
        self.app.include_router(user_router)
        self.app.include_router(sso_router)
        
        # Root endpoint
        @self.app.get("/")
        def root():
            logging.info("Root endpoint was accessed")
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
                logging.info("Database initialized successfully")
            except Exception as e:
                logging.error(f"Error initializing database: {e}")
        
        @self.app.on_event("shutdown")
        def on_shutdown():
            """Cleanup on shutdown"""
            logging.info("Application shutting down")
    
    def get_app(self) -> FastAPI:
        """Get the FastAPI application instance"""
        return self.app


# Create API instance
api = StarWarsAPI()
app = api.get_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 