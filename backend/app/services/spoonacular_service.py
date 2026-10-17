import json
import httpx
from redis.asyncio import Redis
from app.config import settings

SPOONACULAR_BASE_URL = "https://api.spoonacular.com"

async def autocomplete_ingredients(query: str, redis: Redis, number: int = 5) -> list[dict]:
    cache_key = f"autocomplete:{query.lower()}"

    cached = await redis.get(cache_key)
    if cached:
        return json.loads(cached)

    async with httpx.AsyncClient(timeout=5.0) as client:
        response = await client.get(
            f"{SPOONACULAR_BASE_URL}/food/ingredients/autocomplete",
            params={
                "query": query,
                "number": number,
                "apiKey": settings.SPOONACULAR_API_KEY,
            },
        )
        response.raise_for_status()
        results = response.json()

    await redis.set(cache_key, json.dumps(results), ex=86400)
    return results