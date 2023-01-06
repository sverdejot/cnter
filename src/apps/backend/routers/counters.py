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
from Counter.infrastructure.repositories.counter.MotorCounterRepository import MotorCounterRepository
from Counter.domain.value_objects import (
    CounterId,
    UserId,
    CounterPrivate,
)

from dependencies import (
    ClientSession,
    session_maker
)

from .schemas.request.counters import (
    CounterCreateRequestBody,
    CounterIncrementRequestBody,
    CounterJoinRequestBody,
    CounterLeaveRequestBody,
)

router = APIRouter(
    prefix='/counter',
    tags=['counter']
)

@router.get('/{counterId}', status_code=status.HTTP_200_OK)
async def find_counter(counterId: UUID, session: ClientSession = Depends(session_maker)):
    repo = MotorCounterRepository(session)

    finder = CounterFinder(repo=repo)

    counter = await finder(CounterId(counterId))

    if not counter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The counter with id [{counterId}] was not found in the system"
        )

    return {
        'counterId': str(counter.counterId),
        'status': counter.status
    }

@router.post('/{counterId}', status_code=status.HTTP_201_CREATED)
async def create_counter(counterId: UUID, counter: CounterCreateRequestBody, session: ClientSession = Depends(session_maker)):
    repo = MotorCounterRepository(session)

    creator = CounterCreator(repo)

    await creator(counterId=CounterId(counterId), ownerId=UserId(counter.ownerId), private=CounterPrivate(counter.private))

@router.put('/{counterId}/join', status_code=status.HTTP_201_CREATED)
async def join_counter(counterId: UUID, member: CounterJoinRequestBody, session: ClientSession = Depends(session_maker)):
    repo = MotorCounterRepository(session)
    
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
async def increment_counter(counterId: UUID, increment: CounterIncrementRequestBody, session: ClientSession = Depends(session_maker)):
    repo = MotorCounterRepository(session)

    incrementer = CounterIncrementer(repo)

    try:
        await incrementer(CounterId(counterId), UserId(increment.userId))
    except UnauthorizedException:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You are not a member of counter [f{counterId}]. Try to join or ask the owner to invite you."
        )

@router.patch('/{counterId}/leave')
async def leave_counter(counterId: UUID, leave: CounterLeaveRequestBody, session: ClientSession = Depends(session_maker)):
    repo = MotorCounterRepository(session)
    
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