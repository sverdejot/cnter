from .stubs import (
    CounterStub,
    UserStub
)

class TestUser:
    def test_user_can_join_counter(self):
        user = UserStub()
        counter = CounterStub()

        counter.join(user.userId)

        assert user.uid in counter.members
