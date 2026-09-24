import secrets
import string

from cuid import cuid
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from flightagent_mcp.flights.seat_map import get_seat_map
from flightagent_mcp.seats import SeatId

from .errors import (
    booked_seat_error,
    flight_departed_error,
    passenger_mismatch_error,
    unknown_flight_error,
)


class _SeatTakenDuringInsert(Exception):
    pass


async def book_seat(
    session: AsyncSession,
    flight_number: str,
    seat: SeatId,
    passenger_name: str,
    passport: str,
):
    try:
        async with session.begin():
            flight_query = text("""
                SELECT
                    f."id",
                    f."number",
                    f."price",
                    f."deptTime" <=
                        (CURRENT_TIMESTAMP AT TIME ZONE 'UTC') AS has_departed
                FROM "Flight" AS f
                WHERE f."number" = :flight_number
            """)

            flight_result = await session.execute(
                flight_query,
                {"flight_number": flight_number},
            )
            flight = flight_result.mappings().first()

            if flight is None:
                return unknown_flight_error(
                    field="number",
                    flight_number=flight_number,
                )

            if flight["has_departed"]:
                return flight_departed_error(flight_number=flight_number)

            seat_map = await get_seat_map(session, flight_number)
            if seat in seat_map["taken"]:
                return booked_seat_error(
                    flight_number,
                    seat,
                    available=seat_map["available"],
                )

            user_query = text("""
                INSERT INTO "User" ("id", "name", "passport")
                VALUES (:id, :name, :passport)
                ON CONFLICT ("passport") DO NOTHING
                RETURNING "id"
            """)

            user_result = await session.execute(
                user_query,
                {
                    "id": cuid(),
                    "name": passenger_name,
                    "passport": passport,
                },
            )
            user_id = user_result.scalar_one_or_none()

            if user_id is None:
                existing_user_query = text("""
                    SELECT "id", "name"
                    FROM "User"
                    WHERE "passport" = :passport
                """)
                existing_user_result = await session.execute(
                    existing_user_query,
                    {"passport": passport},
                )
                existing_user = existing_user_result.mappings().one()

                if (
                    existing_user["name"].strip().casefold()
                    != passenger_name.strip().casefold()
                ):
                    return passenger_mismatch_error(passenger_name, passport)

                user_id = existing_user["id"]

            # to generate the unique booking reference
            alphabet = string.ascii_uppercase + string.digits
            reference = "".join(secrets.choice(alphabet) for _ in range(6))

            booking_query = text("""
                INSERT INTO "Booking"
                    ("bookingID", "userId", "flightId", "seat", "reference")
                VALUES
                    (:booking_id, :user_id, :flight_id, :seat, :reference)
                ON CONFLICT ("flightId", "seat") DO NOTHING
                RETURNING "bookingID"
            """)

            booking_result = await session.execute(
                booking_query,
                {
                    "booking_id": cuid(),
                    "user_id": user_id,
                    "flight_id": flight["id"],
                    "seat": seat,
                    "reference": reference,
                },
            )

            if booking_result.scalar_one_or_none() is None:
                # this above function returns the first value or none if there are no rows
                # and None here means the seat is already booked because DO NOTHING in the
                # insert query skips the insert if the seat was already booked thus no row
                # to return which we checked with the scalar or none function above
                # winner is decided by who locks commit first like we learned in DB theory
                raise _SeatTakenDuringInsert()

    except _SeatTakenDuringInsert:  # in case of rollback (no new inserts)
        # fetch availability again because another request just took the seat
        current_seat_map = await get_seat_map(session, flight_number)
        return booked_seat_error(
            flight_number,
            seat,
            available=current_seat_map["available"],
        )

    # means the transaction committed successfully
    # again we don't need a manual commit() or close() since we're using the .begin() block
    return {
        "reference": reference,
        "flight": flight_number,
        "seat": seat,
        "price": flight["price"],
    }
