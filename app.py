from fastapi import FastAPI
from routes.character_routes import router as character_router
from routes.eye_color_routes import router as eye_color_router
from routes.keyphrase_routes import router as keyphrase_router
from services.database import init_db

app = FastAPI()

# Inicializar la base de datos
@app.on_event("startup")
def on_startup():
    init_db()

# Incluir routers
app.include_router(character_router)
app.include_router(eye_color_router)
app.include_router(keyphrase_router)


@app.get("/")
def root():
    return {"message": "API de personajes de Star Wars"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 