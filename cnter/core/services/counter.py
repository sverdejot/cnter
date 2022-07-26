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
            'id': owner.id,
            'props': props
        })
        if node := result.single():
            logging.info(f"Succesfully created counter [{node.data().get('counter').get('alias')}]")
            return CounterSchema(**node.data().get('counter'), owner=owner)
        else:
            logging.warn("No return data was found")

def join_counter(user: UserSchema, counter: CounterSchema) -> dict:
    join_query = (
        "MATCH (user:User {uid: $uid}), (counter:Counter {cid: $cid})\n"
        "CREATE (user)-[belong:BELONGS {joined: timestamp(), ts: $ts}]->(counter)\n"
        "RETURN user, belong, counter"
    )
    with db.driver.session() as session:
        result = session.run(
            join_query,
            parameters={
                'cid': counter.id,
                'uid': user.id,
                'joined': datetime.now().timestamp(),
                'ts': []
            }
        )
        if node := result.single():
            return BelongshipSchema(
                user=UserSchema(**node.data().get('user')),
                counter=CounterSchema(**node.data().get('counter')),
                ts=node.data().get('counter').get('joined')
            )
        else:
            logging.warn("No return data was found on join")

def update_counter(username: str, alias: str) -> dict:
    # TODO: save ts of update
    user_belong_query = (
        "MATCH (user:User)-[:BELONGS]->(counter:Counter)\n"
        "WHERE user.username = $username and counter.alias = $alias RETURN counter"
    )

    update_counter_query = (
        "MATCH (counter:Counter)\n"
        "WHERE counter.alias = $alias\n"
        "SET counter.status = $new_status\n"
        "RETURN counter"
    )

    with db.driver.session() as session:
        result = session.run(
            user_belong_query, parameters={
                'username': username, 
                'alias': alias
            })

        if counter := result.single():
            result = session.run(
                update_counter_query,
                parameters={
                    'alias': counter.get('counter').get('alias'),
                    'new_status': counter.get('counter').get('status') + 1
                })
            if node := result.single():
                logging.info(f"User [{username}] updated counter [{node.get('counter').get('alias')}]")
                return node.data()

def delete_counter(username: str, alias: str) -> dict:
    delete_query = (
        "MATCH (user:User {username: $username})-[owner:OWNS]->(counter:Counter {alias: $alias})\n"
        "DELETE owner, counter"
    )

    with db.driver.session() as session:
        result = session.run(delete_query, parameters={
            'username': username,
            'alias': alias
        })
        if result.single():
            logging.info(f"Succesfully deleted")


def get_by_alias(alias: str) -> dict:
    get_query = (
        "MATCH (counter:COUNTER)\n"
        "WHERE counter.alias = $alias"
    )
    with db.driver.session() as session:
        result = session.run(get_query, parameters={
            'alias': alias
        })

        return result.single().data()