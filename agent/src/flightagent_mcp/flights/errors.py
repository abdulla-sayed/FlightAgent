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
