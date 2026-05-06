from fastapi import APIRouter, Depends, HTTPException
import asyncpg
from app.db.connection import get_db
from app.db.queries import search_papers_fts
from app.services.ingestion_service import IngestionService
from app.services.arxiv_client import ArxivClient

router = APIRouter()

@router.get("/search")
async def search(query: str, conn: asyncpg.Connection = Depends(get_db), limit: int = 10):
    try:
        results = await search_papers_fts(conn, query, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

    if results:
        return [dict(row) for row in results]
    else:
        service = IngestionService(ArxivClient())
        await service.ingest_papers(query)
        
        final_results = await search_papers_fts(conn, query, limit)
        if final_results:
            return [dict(row) for row in final_results]
        else:
            raise HTTPException(status_code=404, detail="Error: No results found")
