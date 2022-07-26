from uuid import uuid4
from cnter.core.models.schemas import UserSchema
from cnter.core.config.database import db
import logging

def create_user(user: UserSchema) -> UserSchema:
    cypher_query = (
        "CREATE (user:User {id: $id, username: $username, password: $password})"
        "RETURN user"
    )
    with db.driver.session() as session:
        result = session.run(cypher_query, parameters={'username': user.username, 'id': str(uuid4())
            # TODO: manage password encrypt and store
            , 'password': '1234PaSsWoRd'
        })
        if node := result.single():
            if uid := node.get('user').get('id'):
                logging.info(f"Succesfully created user [{node.data().get('user').get('username')}]")
                return UserSchema(**node.data().get('user'))
        else:
            logging.warn("No return data was found")
