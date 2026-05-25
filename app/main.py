from fastapi import FastAPI
from app.routes.analyze_routes import router as analyze_router


app = FastAPI(
    title="Sentiment Analysis API",
    description="API untuk analisis sentimen guru berdasarkan data request",
    version="1.0.0"
)


app.include_router(analyze_router, prefix="/api", tags=["Analyze"])


@app.get("/")
def root():
    return {
        "success": True,
        "message": "Sentiment Analysis API berjalan"
    }