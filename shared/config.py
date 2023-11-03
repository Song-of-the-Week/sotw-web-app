import os

### GENERAL ###
DEV = os.getenv(key='DEV', default=True)

### DATABASE ###
POSTGRES_USER = os.getenv(key='POSTGRES_USER', default='clarice')
POSTGRES_PASSWORD = os.getenv(key='POSTGRES_PASSWORD', default='password')
POSTGRES_DB = os.getenv(key='POSTGRES_DB', default='sotw')
POSTGRES_URL = 'postgresql://' + POSTGRES_USER + ':' + POSTGRES_PASSWORD + '@localhost:5432/' + POSTGRES_DB if DEV else 'postgresql://' + POSTGRES_USER + ':' + POSTGRES_PASSWORD + '@db:5432/' + POSTGRES_DB