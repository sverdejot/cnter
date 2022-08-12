from cnter.core.domain.model import Counter, User
from cnter.core.adapters.repository.counter import SQLCounterRepository

def insert_user_on_db(session, username='test-username'):
    session.add(User(username=username))
    return session.query(User).filter_by(username=username).one()

def test_repository_can_add_counter(session):
    owner = insert_user_on_db(session, username='test-owner')
    counter = Counter(alias='test-counter', owner=owner)
    repo = SQLCounterRepository(session)

    repo.add(counter)

    assert repo.get(alias='test-counter') == counter

def create_counter(session, alias='test-counter'):
    owner = insert_user_on_db(session, username='test-owner')
    session.add(Counter(owner=owner, alias=alias))
    return session.query(Counter).filter_by(alias=alias).one()

def test_can_update_counter(session):
    counter = create_counter(session)
    member = insert_user_on_db(session, 'test-member')

    counter.members.add(member)
    counter.member_update(member)

    assert counter.state == 1