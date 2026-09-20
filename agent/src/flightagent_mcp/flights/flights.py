from flightagent_mcp.db import engine
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from .errors import unknown_airport_error
from ..db import engine
from .airports import resolve_airports, get_available_cities


async def queryFlights(
    session: AsyncSession, origin: str, destination: str, date: str | None = None
):
    query = text("""
    SELECT
        number,
        "deptTime",
        "arrivalTime",
        price,
        currency,
        "totalSeats" - COUNT("Booking"."bookingID") AS seats_remaining
    FROM
        "Flight"
    LEFT JOIN "Booking"
        ON "Flight"."id" = "Booking"."flightId"
    WHERE
        "originId" = :origin
        AND "destinationId" = :destination
        AND "deptTime" >= :start
        AND "deptTime" < :end
    GROUP BY
        number,
        "deptTime",
        "arrivalTime",
        price,
        currency,
        "totalSeats"
    """)

    if date is None:
        raise RuntimeError("No date can be configured")
    else:
        day = datetime.strptime(date, "%Y-%m-%d")

    result = await session.execute(
        query,
        {
            "origin": origin,
            "destination": destination,
            "start": day,
            "end": day + timedelta(days=1),
        },
    )

    return result.mappings().all()


async def search_flights(
    session: AsyncSession, origin: str, destination: str, date: str | None = None
):
    origin_codes = await resolve_airports(session, origin)
    if not origin_codes:
        cities = await get_available_cities(session)
        return unknown_airport_error(
            field="origin", airport_ref=origin, available_cities=cities
        )

    destination_codes = await resolve_airports(session, destination)
    if not destination_codes:
        cities = await get_available_cities(session)
        return unknown_airport_error(
            field="destination", airport_ref=destination, available_cities=cities
        )

    return await queryFlights(session, origin_codes[0], destination_codes[0], date)
