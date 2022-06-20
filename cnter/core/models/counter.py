from cnter.core.config.database import db
from uuid import uuid4

class Counter:
    @classmethod
    def create_counter(cls, username: str, alias: str, private: bool) -> dict:
        cypher_query = (
            "MATCH (user:User {username: $username})"
            "CREATE (user)-[owner:OWNS]->(counter:Counter $props)\n RETURN counter, owner"
        )
        props = {
            'id': uuid4(),
            'alias': alias,
            'private': private,
            'status': 0
        }
        with db.driver.session() as session:
            result =  session.run(cypher_query, parameters={
                'username': username,
                'props': props
            })
            if node := result.single():
                logging.info(f"Succesfully created counter [{node.data().get('counter').get('alias')}]")
                return node.data()
            else:
                logging.warn("No return data was found")

    @classmethod
    def join_counter(cls, username: str, alias: str) -> dict:
        join_query = (
            "MATCH (user:User {username: $username}), (counter:Counter {alias: $alias})\n"
            "CREATE (user)-[belong:BELONGS {ts: timestamp()}]->(counter)\n"
            "RETURN user, belong, counter"
        )
        with db.driver.session() as session:
            result = session.run(
                join_query,
                parameters={
                    'alias': alias,
                    'username': username,
                }
            )
            if node := result.single():
                logging.info(f"User [{node.data().get('user').get('username')}] joined [{node.data().get('counter').get('alias')}]")
                return node.data()
            else:
                logging.warn("No return data was found on join")

    @classmethod
    def update_counter(cls, username: str, alias: str) -> dict:
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

    @classmethod
    def delete_counter(cls, username: str, alias: str) -> dict:
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


    @classmethod
    def get_by_alias(cls, alias: str) -> dict:
        get_query = (
            "MATCH (counter:COUNTER)\n"
            "WHERE counter.alias = $alias"
        )
        with db.driver.session() as session:
            result = session.run(get_query, parameters={
                'alias': alias
            })

            return result.single().data()