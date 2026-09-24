from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from .errors import booking_not_found_error


# we required both the passport & reference to lessen the surface that random attackers can have
async def get_booking(session: AsyncSession, reference: str, passport: str):
    bookingQuery = text("""
    SELECT
        b."reference",
        b."seat",
        b."timestamp",
        f."number",
        f."price",
        f."deptTime",
        u."name"
    FROM "Booking" AS b
    JOIN "Flight" AS f
        ON f."id" = b."flightId"
    JOIN "User" AS u
        ON u."id" = b."userId"
    WHERE b."reference" = UPPER(:reference)
      AND u."passport" = :passport
    """)

    result = await session.execute(
        bookingQuery,
        {"reference": reference, "passport": passport},
    )
    bookingDetails = result.mappings().first()

    if not bookingDetails:
        return booking_not_found_error(reference)
    else:
        return {
            "ok": True,
            "reference": bookingDetails["reference"],
            "flight": bookingDetails["number"],
            "seat": bookingDetails["seat"],
            "passenger": bookingDetails["name"],
            "price": bookingDetails["price"],
            "timestamp": bookingDetails["timestamp"].isoformat() + "Z",
            "departure_time": bookingDetails["deptTime"].isoformat() + "Z",
        }
