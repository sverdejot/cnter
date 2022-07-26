from cnter.core.models.schemas import UserSchema
from cnter.core.models.schemas import CounterSchema
from uuid import uuid4
from cnter.core.services import userService
from cnter.core.services import counterService

uc = userService.create_user(user=UserSchema(username='sverdejot', password='sVeRdEjOt1234'))

c = counterService.create_counter('#sverdejot', False, uc)

print(c)

