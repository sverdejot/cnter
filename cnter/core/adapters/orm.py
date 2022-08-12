from sqlalchemy import Table, MetaData, Column, Integer, String, ForeignKey
from sqlalchemy.types import Float
from sqlalchemy.orm import registry, relationship

from cnter.core.domain.model import Counter, Update, User

mapper = registry()
metadata = mapper.metadata

users = Table('user', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(30), unique=True)
)

counters = Table('counter', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('alias', String(30), unique=True),
    Column('state', Integer),
    Column('owner_id', Integer, ForeignKey('user.id'), nullable=False)
)

belongships = Table('belongships', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer, ForeignKey('user.id'), nullable=False),
    Column('counter_id', Integer, ForeignKey('counter.id'), nullable=False)
)

updates = Table('updates', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer, ForeignKey('user.id'), nullable=False),
    Column('counter_id', Integer, ForeignKey('counter.id'), nullable=False),
    Column('ts', Float, nullable=False)
)

def start_mappers():
    users_mapper = mapper.map_imperatively(User, users)
    updates_mapper = mapper.map_imperatively(Update, updates)
    counters_mapper = mapper.map_imperatively(Counter, counters, 
        properties={
            'updates': relationship(updates_mapper, collection_class=set),
            'members': relationship(users_mapper, secondary=belongships, collection_class=set),
            'owner': relationship(users_mapper)
        }
    )