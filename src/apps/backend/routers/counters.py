from fastapi import (
    APIRouter,
    status,
    Depends,
    HTTPException
)
from uuid import UUID

from Counter.application.create import CounterCreator
from Counter.application.find import CounterFinder
from Counter.application.join import CounterJoiner
from Counter.application.increment import CounterIncrementer
from Counter.application.leave import CounterLeaver
from Counter.application.kick import CounterKicker
from Counter.domain.exceptions import (
    NotFoundException,
    UnauthorizedException, 
    PrivateException,
    AlreadyMemberException
)
from Counter.domain.value_objects import (
    CounterId,
    UserId,
    CounterPrivate,
)
from Counter.infrastructure.repositories.counter import uMongoCounterRepository

from .schemas.request.counters import (
    CounterCreateRequestBody,
    CounterIncrementRequestBody,
    CounterJoinRequestBody,
    CounterLeaveRequestBody,
)

from .schemas.response.counters import(
    CounterFindReponseBody
)

router = APIRouter(
    prefix='/counter',
    tags=['counter']
)

@router.get('/{counterId}', status_code=status.HTTP_200_OK)
async def find_counter(counterId: UUID):
    repo = uMongoCounterRepository()

    finder = CounterFinder(repo=repo)

    try:
        counter = await finder(CounterId(counterId))
    except NotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The counter with id [{counterId}] was not found in the system"
        )

    return CounterFindReponseBody(
        counterId=counter.counterId.value,
        ownerId=counter.ownerId.value,
        status=counter.status,
        private=counter.private,
        members=[
            memberId.value for memberId in counter.members
        ]
    )

@router.post('/{counterId}', status_code=status.HTTP_201_CREATED)
async def create_counter(counterId: UUID, counter: CounterCreateRequestBody):
    repo = uMongoCounterRepository()

    creator = CounterCreator(repo)

    await creator(counterId=CounterId(counterId), ownerId=UserId(counter.ownerId), private=CounterPrivate(counter.private))

@router.put('/{counterId}/join', status_code=status.HTTP_201_CREATED)
async def join_counter(counterId: UUID, member: CounterJoinRequestBody):
    repo = uMongoCounterRepository()
    
    joiner = CounterJoiner(repo)
    try:
        await joiner(CounterId(counterId), UserId(member.userId))
    except AlreadyMemberException:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"The user with id [{member.userId}] is already a member"
        )
    except PrivateException:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"The specified counter is private. Ask the owner to invite you"
        )


@router.put('/{counterId}/increment', status_code=status.HTTP_200_OK)
async def increment_counter(counterId: UUID, increment: CounterIncrementRequestBody):
    repo = uMongoCounterRepository()

    incrementer = CounterIncrementer(repo)

    try:
        await incrementer(CounterId(counterId), UserId(increment.userId))
    except UnauthorizedException:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You are not a member of counter [f{counterId}]. Try to join or ask the owner to invite you."
        )

@router.patch('/{counterId}/leave')
async def leave_counter(counterId: UUID, leave: CounterLeaveRequestBody):
    repo = uMongoCounterRepository()
    
    if not leave.ownerId:
        leaver = CounterLeaver(repo)
        
        await leaver(counterId=CounterId(counterId), memberId=UserId(leave.memberId))
    else:
        kicker = CounterKicker(repo)
        try:
            await kicker(ownerId=UserId(leave.ownerId), counterId=CounterId(counterId), memberId=UserId(leave.memberId))
        except UnauthorizedException:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Only owner of counter [{counterId}] is allowed to kick members"
            )