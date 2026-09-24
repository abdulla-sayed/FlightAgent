from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from flightagent_mcp.seats import render_seat_map, SEAT_IDS

from .errors import unknown_flight_error


async def get_seat_map(session: AsyncSession, flight_number: str):
    flightQuery = text("""
    SELECT
        f."number",
        b."seat"
    FROM "Flight" AS f
    LEFT JOIN "Booking" AS b
        ON f."id" = b."flightId"
    WHERE f."number" = :flight_number
    """)

    result = await session.execute(flightQuery, {"flight_number": flight_number})
    flight = result.mappings().all()

    if not flight:
        return unknown_flight_error(field="number", flight_number=flight_number)

    taken = []
    for booking in flight:
        if booking["seat"] is not None:
            taken.append(booking["seat"])

    taken = set(taken)
    available = []

    for seat in SEAT_IDS:
        if seat not in taken:
            available.append(seat)

    return {
        "ascii": render_seat_map(taken),
        "taken": [seat for seat in SEAT_IDS if seat in taken],
        "available": available,
    }
