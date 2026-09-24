import os
from typing import Literal

from dotenv import load_dotenv
from fastmcp import FastMCP

from flightagent_mcp.flights.book_seat import (
    book_seat,
)
from flightagent_mcp.flights.get_booking import get_booking
from flightagent_mcp.flights.seat_map import get_seat_map
from flightagent_mcp.seats import SeatId
from fastmcp.exceptions import ResourceError

load_dotenv()

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from flightagent_mcp.db import engine
from flightagent_mcp.flights.flights import (
    search_flights as search_flights_service,
)

mcp = FastMCP(name="flightagent")

Transport = Literal["stdio", "http", "sse", "streamable-http"]


@mcp.tool()
async def search_flights(
    origin: str,
    destination: str,
    date: str | None = None,
):
    """Search for flights by city name or IATA airport code.

    Date should be formatted as YYYY-MM-DD.
    """

    async with AsyncSession(engine) as session:
        return await search_flights_service(
            session=session,
            origin=origin,
            destination=destination,
            date=date,
        )


@mcp.tool()
async def render_flight(flight_number: str):
    """Show the seat map and available seats for a flight number.

    Returns the ASCII seat map plus separate lists of available and taken
    seat IDs. Returns a structured error if the flight number is unknown.
    """

    async with AsyncSession(engine) as session:
        return await get_seat_map(session, flight_number)


@mcp.tool()
async def book_flight(
    flight_number: str,
    seat: SeatId,
    passenger_name: str,
    passport: str,
):
    """Book a seat for a passenger on a flight.

    Returns the booking reference, flight, seat, and price on success.
    Returns a structured error if the flight or seat cannot be booked.
    """
    async with AsyncSession(engine) as session:
        return await book_seat(session, flight_number, seat, passenger_name, passport)


@mcp.tool()
async def read_booking(
    reference: str,
    passport: str,
):
    """Look up a booking using its reference and the passenger's passport.

    The reference is case-insensitive. Returns the flight, seat, passenger,
    price, booking timestamp, and departure time when both inputs match.
    Returns a structured error when no matching booking is found.
    """

    async with AsyncSession(engine) as session:
        return await get_booking(session, reference, passport)


@mcp.tool()
def greet():
    return "Hello world!"


@mcp.resource("flightagent://policy/booking", mime_type="text/markdown")
def booking_policy_resource() -> str:
    """Booking, baggage, change, and refund policy for the simulation."""
    return """# Flightagent booking policy


## Baggage
no baggage allowed bro.

## Changes and refunds
nah no refunds here tbh

## Simulation Notice
this is all a simulation you are not welcome here and why are you even using this thing? get a life
"""


@mcp.resource("flightagent://flights/{number}", mime_type="application/json")
async def flight_resource(number: str) -> dict:
    """List details of a specific flight using its number."""
    async with AsyncSession(engine) as session:
        flightQuery = text("""
        SELECT
            f."number",
            f."originId",
            f."destinationId",
            f."deptTime",
            f."arrivalTime",
            f."price",
            f."currency",
            f."totalSeats"
        FROM "Flight" AS f
        WHERE f."number" = :number
        """)

        result = await session.execute(flightQuery, {"number": number})
        flightResolved = result.mappings().first()

        if not flightResolved:
            raise ResourceError(f"Flight with number {number} does not exist.")
        else:
            return {
                "number": flightResolved["number"],
                "origin": flightResolved["originId"],
                "destination": flightResolved["destinationId"],
                "departure_time": flightResolved["deptTime"].isoformat() + "Z",
                "arrival_time": flightResolved["arrivalTime"].isoformat() + "Z",
                "price": flightResolved["price"],
                "currency": flightResolved["currency"],
                "total_seats": flightResolved["totalSeats"],
            }


@mcp.resource("flightagent://airports", mime_type="application/json")
async def airports_resource() -> list[dict]:
    """List the airports available in the flight simulation."""
    async with AsyncSession(engine) as session:
        airportQuery = text("""
            SELECT "code", "name", "city"
            FROM "Airport"
            ORDER BY "city", "code"
        """)

        result = await session.execute(airportQuery)
        airports = result.mappings().all()

        return [
            {
                "code": airport["code"],
                "name": airport["name"],
                "city": airport["city"],
            }
            for airport in airports
        ]


def main() -> None:
    transport = os.getenv("TRANSPORT_MODE", "stdio")

    if transport not in ("stdio", "http", "sse", "streamable-http"):
        raise ValueError(f"Invalid TRANSPORT_MODE: {transport}")

    if transport == "stdio":
        mcp.run(transport="stdio")
    else:
        mcp.run(
            transport=transport,
            host="0.0.0.0",
            port=8001,  # this is just a placeholder for now, as it could collide with FastAPI later.
        )


if __name__ == "__main__":
    main()
