--> python3 -m venv myvenv

## here we have to create our virtual environment

## in order to start the virtual environment

--> source myvenv/bin/activate

## installed all the libraries that are in the file

pip install -r requirements.txt

## to connect to the DB we can use

psql -U postgres -h localhost -p 5434 -d daily_tracker
CREATE USER tracker_user WITH PASSWORD 'dev_password';
GRANT ALL PRIVILEGES ON DATABASE daily_tracker TO tracker_user;

## to modernize the DB setup

pip install sqlalchemy asyncpg

## to generate the new migration we can use

# we use the alembit to track the changes in the DB structure [like git for out DB]

# the revision compares our current models , compares the current Db schema detect differences and create a migration file [instruction to change the DB schema]

alembic revision --autogenerate -m "create_users_table"

## then to migrate

#

alembic upgrade head

## for the access token and the refresh token

we have to use the strong SECRET_KEY generated via " openssl rand -hex 32 "

Never put sensitive data in the payload. use the " sub " claim for the user_id

for web apps often its safe to store the refresh token in HTTPOnly cookie to prevent attacks

## setting up the mcp server

pip install "mcp[cli]"

# or using uv

uv add "mcp[cli]"

## Initialize the mcp server

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("My FastAPI MCP Server")

@mcp.tool()
def calculate_sum(a: int, b: int) -> int:
"""Adds two numbers together."""
return a + b


## working witht the mcp server
# mcp tool functions are stand alone 