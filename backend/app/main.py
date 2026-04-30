from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup: We will initialize DB and Redis connections here later
    print("System starting up...")
    yield
    # Teardown: Close connections here
    print("System shutting down...")

app = FastAPI(
    title="Paper Intelligence API",
    description="Scalable document ingestion, search, and ranking backend",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/health")
async def health_check():
    """Basic health check endpoint for observability/load balancers."""
    return {"status": "ok", "service": "paper-intelligence-backend"}
