import os

from dotenv import load_dotenv
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import create_async_engine

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise RuntimeError("Environment is not correctly configured.")

database_url = make_url(DATABASE_URL)
database_url = database_url.set(drivername="postgresql+asyncpg")

# Adapt Prisma/libpq connection options for asyncpg
# This changes only the local SQLAlchemy URL, not DATABASE_URL itself
query_options = dict(database_url.query)

# asyncpg expects "ssl", not "sslmode".
ssl_mode = query_options.pop("sslmode", None)

# asyncpg does not accept "channel_binding" as a connection argument
query_options.pop("channel_binding", None)

database_url = database_url.set(query=query_options)

connect_args = {}

if ssl_mode:
    connect_args["ssl"] = ssl_mode

engine = create_async_engine(
    database_url,
    connect_args=connect_args,
    echo=True,
)
