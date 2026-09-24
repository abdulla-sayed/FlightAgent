from flightagent_mcp.seats import SeatId


def unknown_airport_error(
    field: str,
    airport_ref: str,
    available_cities: list[str],
) -> dict:
    return {
        "ok": False,
        "error": {
            "code": "UNKNOWN_AIRPORT",
            "field": field,
            "input": airport_ref,
            "message": (
                f"Unknown {field} '{airport_ref}'. " "Use a valid city or IATA code."
            ),
            "available_cities": available_cities,
        },
    }


def unknown_flight_error(field: str, flight_number: str):
    return {
        "ok": False,
        "error": {
            "code": "UNKNOWN_FLIGHT",
            "field": field,
            "input": flight_number,
            "message": (
                f"Unknown {field} '{flight_number}'. " "Use a valid flight number."
            ),
        },
    }


def flight_departed_error(flight_number: str):
    return {
        "ok": False,
        "error": {
            "code": "FLIGHT_DEPARTED",
            "input": flight_number,
            "message": (f"Flight {flight_number} has already departed."),
        },
    }


def booked_seat_error(flight_number: str, seat: SeatId, available: list[str]):
    return {
        "ok": False,
        "error": {
            "code": "SEAT_TAKEN",
            "input": {
                "flight_number": flight_number,
                "seat": seat,
            },
            "message": f"Seat {seat} on {flight_number} is already booked.",
            "available": available,  # can be used by the agent to inform user
        },
    }


def passenger_mismatch_error(passenger_name: str, passport: str):
    return {
        "ok": False,
        "error": {
            "code": "PASSENGER_DETAILS_MISMATCH",
            "input": {
                "passenger_name": passenger_name,
                "passport": passport,
            },
            "message": (
                "The passenger name does not match the "
                "existing record for this passport."
            ),
        },
    }


def booking_not_found_error(reference: str):
    return {
        "ok": False,
        "error": {
            "code": "BOOKING_NOT_FOUND",
            "input": {"reference": reference},
            "message": "No booking found for the supplied reference and passport.",
        },
    }
