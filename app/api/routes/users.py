#  Copyright 2022 Pavel Suprunov
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from typing import Optional

from fastapi import (
    APIRouter,
    Body,
    Depends,
    HTTPException,
    status, Query,
)

from app.api.dependencies.authentication import get_current_user_authorizer, get_current_user_is_admin
from app.api.dependencies.database import get_repository
from app.database.errors import EntityDoesNotExists
from app.database.repositories.users import UsersRepository
from app.database.repositories.verification_codes import VerificationRepository
from app.models.domain.user import UserInDB
from app.models.schemas.location import LocationInCreate
from app.models.schemas.user import (
    UserInResponse,
    UserInUpdate,
)
from app.resources import strings
from app.services.authentication import (
    check_phone_is_valid,
    check_phone_is_taken,
    check_username_is_taken,
)

router = APIRouter()


@router.get(
    "",
    response_model=UserInResponse,
    name="users:get-current-user"
)
async def get_current_user(
        user: UserInDB = Depends(get_current_user_authorizer()),
) -> UserInResponse:
    return UserInResponse(user=user)


@router.put(
    "",
    response_model=UserInResponse,
    name="users:update-current-user"
)
async def update_current_user(
        user_update: UserInUpdate = Body(..., embed=True, alias="user"),
        user: UserInDB = Depends(get_current_user_authorizer()),
        users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
        verification_repo: VerificationRepository = Depends(get_repository(VerificationRepository)),
) -> UserInResponse:
    phone_invalid = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=strings.PHONE_NUMBER_INVALID_ERROR
    )
    phone_taken = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=strings.PHONE_TAKEN
    )
    verification_code_wrong = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=strings.VERIFICATION_CODE_IS_WRONG
    )
    username_taken = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=strings.USERNAME_TAKEN
    )

    if user_update.phone and user_update.phone != user.phone:
        if not check_phone_is_valid(user_update.phone):
            raise phone_invalid

        if await check_phone_is_taken(users_repo, user_update.phone):
            raise phone_taken

        try:
            await verification_repo.get_verification_code_by_phone_and_code(
                user_update.phone,
                user_update.verification_code
            )
        except EntityDoesNotExists as exception:
            raise verification_code_wrong from exception

    if user_update.username and user_update.username != user.username:
        if await check_username_is_taken(users_repo, user_update.username):
            raise username_taken

    user_in_db = await users_repo.update_user_by_user(
        user.id,
        phone=user_update.phone,
        username=user_update.username,
        password=user_update.password,
    )

    return UserInResponse(user=user_in_db)


@router.get(
    "/mark_as_admin",
    response_model=UserInResponse,
    name="users:mark-user-as-admin",
    dependencies=[
        Depends(get_current_user_is_admin())
    ]
)
async def mark_user_as_admin(
        user: UserInDB = Depends(get_current_user_authorizer()),
        users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
) -> UserInResponse:
    user_update_error = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=strings.PERMISSION_DENIED
    )

    try:
        user = await users_repo.set_user_by_id_as_admin(user.id, True)
    except EntityDoesNotExists as exception:
        raise user_update_error from exception

    return UserInResponse(user=user)


@router.get(
    "/unmark_as_admin",
    response_model=UserInResponse,
    name="users:unmark-user-as-admin",
    dependencies=[
        Depends(get_current_user_is_admin())
    ]
)
async def unmark_user_as_admin(
        user: UserInDB = Depends(get_current_user_authorizer()),
        users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
) -> UserInResponse:
    user_update_error = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=strings.PERMISSION_DENIED
    )

    try:
        user = await users_repo.set_user_by_id_as_admin(user.id, False)
    except EntityDoesNotExists as exception:
        raise user_update_error from exception

    return UserInResponse(user=user)


@router.get(
    "/mark_as_blocked",
    response_model=UserInResponse,
    name="users:mark-user-as-blocked",
)
async def mark_user_as_blocked(
        user: UserInDB = Depends(get_current_user_authorizer()),
        users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
) -> UserInResponse:
    user_update_error = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=strings.PERMISSION_DENIED
    )

    try:
        user = await users_repo.set_user_by_id_is_blocked(user.id, True)
    except EntityDoesNotExists as exception:
        raise user_update_error from exception

    return UserInResponse(user=user)


@router.get(
    "/unmark_as_blocked",
    response_model=UserInResponse,
    name="users:unmark-user-as-blocked",
)
async def unmark_user_as_blocked(
        user: UserInDB = Depends(get_current_user_authorizer()),
        users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
) -> UserInResponse:
    user_update_error = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=strings.PERMISSION_DENIED
    )

    try:
        user = await users_repo.set_user_by_id_is_blocked(user.id, False)
    except EntityDoesNotExists as exception:
        raise user_update_error from exception

    return UserInResponse(user=user)


@router.post(
    "/update_current_location",
    response_model=UserInResponse,
    name="users:update-current-location",
)
async def update_current_location(
        location_create: LocationInCreate = Body(..., embed=True, alias="location"),
        user: UserInDB = Depends(get_current_user_authorizer()),
        users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
) -> UserInResponse:
    user_update_error = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=strings.PERMISSION_DENIED
    )

    try:
        user = await users_repo.set_user_by_id_is_blocked(user.id, False)
    except EntityDoesNotExists as exception:
        raise user_update_error from exception

    return UserInResponse(user=user)
