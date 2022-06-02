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

from fastapi import APIRouter, status, Depends

from app.api.dependencies.authentication import get_current_user_authorizer
from app.api.dependencies.database import get_repository
from app.api.dependencies.services_types import get_service_type_id_from_path
from app.database.repositories.services_types import ServicesTypesRepository
from app.models.domain.service import Service
from app.models.domain.user import UserInDB
from app.models.schemas.service_type import ServiceTypeInResponse, ListOfServicesTypesInResponse

router = APIRouter()


@router.get("", response_model=ListOfServicesTypesInResponse, name="services-types:get-all-vehicles")
async def get_service_types(
        user: UserInDB = Depends(get_current_user_authorizer()),
        services_types_repo: ServicesTypesRepository = Depends(get_repository(ServicesTypesRepository)),
) -> ListOfServicesTypesInResponse:
    services_types = await services_types_repo.get_services_types(user)
    return ListOfServicesTypesInResponse(services_types=services_types, count=len(services_types))


@router.post("", response_model=ServiceTypeInResponse, name="services-types:create-vehicle")
async def create_service_type() -> ServiceTypeInResponse:
    pass


@router.get("/{type_id}", response_model=ServiceTypeInResponse, name="services-types:get-vehicle")
async def get_service_type(
        type_id: int = Depends(get_service_type_id_from_path),
) -> ServiceTypeInResponse:
    pass


@router.put("/{type_id}", response_model=ServiceTypeInResponse, name="services-types:update-vehicle")
async def update_service_type(
        type_id: int = Depends(get_service_type_id_from_path),
) -> ServiceTypeInResponse:
    pass


@router.delete("/{type_id}", response_model=ServiceTypeInResponse, name="services-types:delete-vehicle")
async def delete_service_type(
        type_id: int = Depends(get_service_type_id_from_path),
) -> ServiceTypeInResponse:
    pass