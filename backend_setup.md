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
