import os
from typing import Literal

from dotenv import load_dotenv
from fastmcp import FastMCP

from flightagent_mcp.flights.seat_map import get_seat_map

load_dotenv()

from sqlalchemy.ext.asyncio import AsyncSession

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


@mcp.tool()
def greet():
    return "Hello world!"


if __name__ == "__main__":
    main()
