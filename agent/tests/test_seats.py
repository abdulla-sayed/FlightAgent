from flightagent_mcp.seats import SEAT_IDS, render_seat_map


def test_render_seat_map_empty_cabin():
    assert render_seat_map(set()) == (
        "Row 1   1A  1B  1C \n"
        "         o   o   o  \n"
        "\n"
        "Row 2   2A  2B  2C \n"
        "         o   o   o  \n"
        "\n"
        "o = available   x = unavailable"
    )


def test_render_seat_map_full_cabin():
    assert render_seat_map(set(SEAT_IDS)) == (
        "Row 1   1A  1B  1C \n"
        "         x   x   x  \n"
        "\n"
        "Row 2   2A  2B  2C \n"
        "         x   x   x  \n"
        "\n"
        "o = available   x = unavailable"
    )


def test_render_seat_map_one_seat_taken():
    assert render_seat_map({"1B"}) == (
        "Row 1   1A  1B  1C \n"
        "         o   x   o  \n"
        "\n"
        "Row 2   2A  2B  2C \n"
        "         o   o   o  \n"
        "\n"
        "o = available   x = unavailable"
    )
