from uuid import uuid4

class User:
    @classmethod
    def create_user(self, username: str) -> dict:
        cypher_query = ("CREATE (u:User {id: $id: $username}) RETURN u")
        with db.driver.session() as session:
            result = session.run(cypher_query, parameters={'username': username, 'id': uuid4()})
            if node := result.single():
                logging.info(f"Succesfully created counter [{node.data().get('alias')}]")
                return node.data()
            else:
                logging.warn("No return data was found")