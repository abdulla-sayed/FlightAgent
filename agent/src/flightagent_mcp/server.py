import os
from typing import Literal

from dotenv import load_dotenv
from fastmcp import FastMCP

load_dotenv()

mcp = FastMCP(name="flightagent")

Transport = Literal["stdio", "http", "sse", "streamable-http"]


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
