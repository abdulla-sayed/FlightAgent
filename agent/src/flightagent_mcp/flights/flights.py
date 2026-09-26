from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta, timezone
from .errors import invalid_date_error, unknown_airport_error
from .airports import resolve_airports, get_available_cities


def parse_day(value: str) -> datetime:
    return datetime.strptime(value, "%Y-%m-%d")


async def queryFlights(
    session: AsyncSession,
    origin: str,
    destination: str,
    start: datetime | None = None,
    end: datetime | None = None,
):
    # start is inclusive, end is exclusive; either can be left open
    conditions = ['"originId" = :origin', '"destinationId" = :destination']
    params: dict = {"origin": origin, "destination": destination}

    if start is not None:
        conditions.append('"deptTime" >= :start')
        params["start"] = start
    if end is not None:
        conditions.append('"deptTime" < :end')
        params["end"] = end

    query = text(f"""
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
        {" AND ".join(conditions)}
    GROUP BY
        number,
        "deptTime",
        "arrivalTime",
        price,
        currency,
        "totalSeats"
    ORDER BY
        "deptTime"
    """)

    result = await session.execute(query, params)

    return [dict(row) for row in result.mappings().all()]


async def search_flights(
    session: AsyncSession,
    origin: str,
    destination: str,
    date: str | None = None,
    departs_after: str | None = None,
    departs_before: str | None = None,
    include_past: bool = False,
):
    if date is not None and (departs_after is not None or departs_before is not None):
        return invalid_date_error(
            field="date",
            value=date,
            message="Use either 'date' or 'departs_after'/'departs_before', not both.",
        )

    # parse every supplied date up front so a bad value is reported by name
    parsed: dict[str, datetime] = {}
    for field, value in (
        ("date", date),
        ("departs_after", departs_after),
        ("departs_before", departs_before),
    ):
        if value is None:
            continue
        try:
            parsed[field] = parse_day(value)
        except ValueError:
            return invalid_date_error(field=field, value=value)

    if "date" in parsed:
        start = parsed["date"]
        end = start + timedelta(days=1)
    else:
        start = parsed.get("departs_after")
        # departs_before is inclusive of that whole day
        end = (
            parsed["departs_before"] + timedelta(days=1)
            if "departs_before" in parsed
            else None
        )

    if start is not None and end is not None and start >= end:
        return invalid_date_error(
            field="departs_before",
            value=departs_before or "",
            message="'departs_before' must be on or after 'departs_after'.",
        )

    if not include_past:
        # deptTime is stored as a naive UTC timestamp
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        start = now if start is None else max(start, now)

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

    flights = await queryFlights(
        session, origin_codes[0], destination_codes[0], start, end
    )

    return {"ok": True, "count": len(flights), "flights": flights}
