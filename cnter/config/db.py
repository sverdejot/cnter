from dotenv import find_dotenv, load_dotenv
from sqlalchemy import create_engine
from cnter.core.adapters.orm import metadata, start_mappers
import os

env_file = find_dotenv('.env')
load_dotenv(env_file)

def get_mariadb_uri():
    user = os.environ.get('MARIADB_USER')
    psswd = os.environ.get('MARIADB_PSSWD')
    port = os.environ.get('MARIADB_PORT')
    uri = os.environ.get('MARIADB_URI')

    return f"mariadb+mariadbconnector://{user}:{psswd}@{uri}:{port}/cnter"

engine = create_engine(get_mariadb_uri(), isolation_level='REPEATABLE READ')
metadata.create_all(engine)