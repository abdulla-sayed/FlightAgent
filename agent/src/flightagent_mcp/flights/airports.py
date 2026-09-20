from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List


async def resolve_airports(session: AsyncSession, airport_ref: str) -> List[str]:
    query = text("""
    SELECT 
        code
    FROM
        "Airport"
    WHERE
        LOWER(city) = LOWER(:airport_ref)
    OR
        LOWER(code) = LOWER(:airport_ref)
    """)

    result = await session.execute(query, {"airport_ref": airport_ref.strip()})

    return list(result.scalars().all())


async def get_available_cities(session: AsyncSession) -> List[str]:
    query = text("""
    SELECT DISTINCT
        city
    FROM
        "Airport"
    ORDER BY
        city
    """)

    result = await session.execute(query)

    return list(result.scalars().all())
