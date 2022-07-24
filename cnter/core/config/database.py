from neo4j import GraphDatabase
from dotenv import load_dotenv, find_dotenv
import os
import logging

class Database:
    def __init__(self, uri, user, password):
        try:
            self.driver = GraphDatabase.driver(uri=uri, auth=(user, password))
        except Exception as err:
            logging.error(f"[FATAL] Could not initialize database: \t {err}")

env_var = find_dotenv('.env')
load_dotenv(env_var)

db = Database(
    uri=os.environ.get('NEO4J_DB_URI'),
    user=os.environ.get('NEO4J_DB_ADMIN_USERNAME'),
    password=os.environ.get('NEO4J_DB_ADMIN_PASSWORD')
)