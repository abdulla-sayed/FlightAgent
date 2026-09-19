SEAT_IDS = ("1A", "1B", "1C", "2A", "2B", "2C")

AVAILABLE_MARKER = "o"
UNAVAILABLE_MARKER = "x"

_ROWS = (SEAT_IDS[0:3], SEAT_IDS[3:6])
_COLUMN_WIDTH = 4


def render_seat_map(taken: set[str]) -> str:
    lines: list[str] = []

    for row_number, row in enumerate(_ROWS, start=1):
        seat_labels = "".join(seat.center(_COLUMN_WIDTH) for seat in row)
        markers = "".join(
            (UNAVAILABLE_MARKER if seat in taken else AVAILABLE_MARKER).center(
                _COLUMN_WIDTH
            )
            for seat in row
        )
        lines.append(f"Row {row_number}  {seat_labels}")
        lines.append(f"        {markers}")
        lines.append("")

    lines.append(f"{AVAILABLE_MARKER} = available   {UNAVAILABLE_MARKER} = unavailable")

    return "\n".join(lines)
