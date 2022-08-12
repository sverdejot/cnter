from cnter.core.domain.model import User, Counter

def generate_counter():
    return Counter(
        alias='test-counter',
        owner=User(
            username='test-owner'
        )
    )

def test_user_can_join():
    user = User(username='test-member')
    counter = generate_counter()

    result = counter.join(user)

    assert result == True
    assert user in counter.members

def test_member_cant_rejoin():
    member = User(username='test-member')
    counter = generate_counter()

    counter.join(member)

    # try to rejoin
    assert not counter.join(member)

def test_owner_cant_join():
    owner = User(username='test-owner')
    counter = generate_counter()

    assert not counter.join(owner)

def test_member_can_update():
    member = User(username='test-member')
    counter = generate_counter()

    # add to members
    counter.members.add(member)

    counter.member_update(member)

    assert counter.state == 1