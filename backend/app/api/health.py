from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.core.database import get_db
from app.core.redis import get_redis_client
from app.services.ai import provider_manager
from app.schemas import HealthCheck

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthCheck)
async def health_check(db: AsyncSession = Depends(get_db)):
    """Health check endpoint."""
    
    # Check database
    db_status = "healthy"
    try:
        await db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
    
    # Check Redis
    redis_status = "healthy"
    try:
        redis_client = await get_redis_client()
        await redis_client.ping()
    except Exception as e:
        redis_status = f"unhealthy: {str(e)}"
    
    # Check AI providers
    providers = provider_manager.get_available_providers()
    
    return HealthCheck(
        status="healthy" if db_status == "healthy" and redis_status == "healthy" else "degraded",
        database=db_status,
        redis=redis_status,
        providers=providers
    )
