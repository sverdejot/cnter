from cnter.core.config.database import db

from cnter.core.models.schemas import UserSchema
from cnter.core.models.schemas import CounterSchema
from cnter.core.models.schemas import BelongshipSchema

from uuid import uuid4
from datetime import datetime
import logging

def create_counter(alias: str, private: bool, owner: UserSchema) -> CounterSchema:
    cypher_query = (
        "MATCH (user:User {id: $id})"
        "CREATE (user)-[owner:OWNS]->(counter:Counter $props)\n RETURN counter, owner"
    )
    props = {
        'id': str(uuid4()),
        'alias': alias,
        'private': private,
        'status': 0
    }
    with db.driver.session() as session:
        result = session.run(cypher_query, parameters={
            'id': str(owner.id),
            'props': props
        })
        if node := result.single():
            logging.info(f"Succesfully created counter [{node.data().get('counter').get('alias')}]")
            return CounterSchema(**node.data().get('counter'), owner=owner)
        else:
            logging.warn("No return data was found")

def join_counter(user: UserSchema, counter: CounterSchema) -> dict:
    join_query = (
        "MATCH (user:User {id: $uid}), (counter:Counter {id: $cid})\n"
        "CREATE (user)-[belong:BELONGS {joined: timestamp(), ts: $ts}]->(counter)\n"
        "RETURN user, belong, counter"
    )
    with db.driver.session() as session:
        result = session.run(
            join_query,
            parameters={
                'cid': str(counter.id),
                'uid': str(user.id),
                'joined': datetime.now().timestamp(),
                'ts': []
            }
        )
        if node := result.single():
            return BelongshipSchema(
                user=UserSchema(**node.data().get('user')),
                counter=CounterSchema(**node.data().get('counter'), owner=UserSchema(**node.data().get('user'))),
                ts=[float(ts) for ts in node.get('belong').get('ts')],
                joined=float(node.get('belong').get('joined'))
            )
        else:
            logging.warn("No return data was found on join")

def update_counter(belongship: BelongshipSchema) -> BelongshipSchema:
    cypher_query = (
        "MATCH (user:User)-[belong:BELONGS]->(counter:Counter)\n"
        "WHERE user.id = $uid and counter.id = $cid\n"
        "SET counter.status = counter.status + 1\n"
        "SET belong.ts = belong.ts + [$ts]\n"
        "RETURN user, belong, counter"
    )

    with db.driver.session() as session:
        result = session.run(
            cypher_query, parameters={
                'uid': str(belongship.user.id), 
                'cid': str(belongship.counter.id),
                'ts': float(datetime.now().timestamp())
            })

        if node := result.single():
            return BelongshipSchema(
                ts=node.get('belong').get('ts'),
                joined=node.get('belong').get('joined'),
                user=UserSchema(**node.data().get('user')),
                counter=CounterSchema(**node.data().get('counter'), owner=UserSchema(**node.data().get('user')))
            )
            

def delete_counter(counter: CounterSchema) -> bool:
    delete_query = (
        "MATCH (counter:User {id: $cid})\n"
        "DETACH DELETE counter"
    )

    with db.driver.session() as session:
        result = session.run(delete_query, parameters={
            'cid': counter.id
        })
        if result.single():
            logging.info(f"Succesfully deleted")
            return True
        else:
            return False


def get_by_alias(alias: str) -> CounterSchema:
    get_query = (
        "MATCH (user:User)-[:OWNS]->(counter:Counter)\n"
        "WHERE counter.alias = $alias RETURN counter, user"
    )
    with db.driver.session() as session:
        result = session.run(get_query, parameters={
            'alias': alias
        })

        if node := result.single():
            return CounterSchema(
                **node.data().get('counter'),
                owner=UserSchema(**node.data().get('user'))
            )