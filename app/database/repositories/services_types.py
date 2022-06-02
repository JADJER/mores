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
from typing import List, Optional

from sqlalchemy import select, and_

from app.database.errors import EntityDoesNotExist
from app.database.models import ServiceTypeModel
from app.database.repositories.base import BaseRepository
from app.models.domain.service_type import ServiceType
from app.models.domain.user import UserInDB


class ServicesTypesRepository(BaseRepository):

    async def get_service_type_model_by_id(self, user: UserInDB, service_type_id: int) -> ServiceTypeModel:
        query = select(ServiceTypeModel).where(
            and_(
                ServiceTypeModel.owner_id == user.id,
                ServiceTypeModel.id == service_type_id
            )
        )
        result = await self.session.execute(query)

        service_type_in_db: ServiceTypeModel = result.scalars().first()
        if not service_type_in_db:
            raise EntityDoesNotExist("vehicle with id {} does not exist".format(service_type_id))

        return service_type_in_db

    async def get_service_type_by_id(self, user: UserInDB, vehicle_id: int) -> ServiceType:
        service_type_model = await self.get_service_type_model_by_id(user, vehicle_id)
        return ServiceType(**service_type_model.__dict__)

    async def get_services_types(self, user: UserInDB) -> List[ServiceType]:
        query = select(ServiceTypeModel).where(ServiceTypeModel.owner_id == user.id)
        result = await self.session.execute(query)

        services_types_in_db = result.scalars().all()

        return [ServiceType(**service_type_in_db.__dict__) for service_type_in_db in services_types_in_db]

    async def create_service_type(
            self,
            user: UserInDB,
            *,
            name: str,
            description: str,
    ) -> ServiceType:
        new_service_type = ServiceTypeModel()
        new_service_type.name = name
        new_service_type.description = description

        try:
            self.session.add(new_service_type)
            await self.session.commit()

        except Exception:
            raise VehicleAlreadyExist("Conflict vin or registration plate")

        return ServiceType(**new_service_type.__dict__)

    async def update_service_type(
            self,
            user: UserInDB,
            vehicle_id: int,
            *,
            name: Optional[str],
            description: Optional[str],
    ) -> ServiceType:
        service_type = await self.get_service_type_model_by_id(user, vehicle_id)
        service_type.name = name or service_type.name
        service_type.description = description or service_type.description

        try:
            await self.session.commit()

        except Exception:
            raise VehicleAlreadyExist("Conflict vin or registration plate")

        return Vehicle(**vehicle.__dict__)

    async def delete_service_type(self, user: UserInDB, vehicle_id: int) -> None:
        vehicle = await self.get_vehicle_model_by_id(user, vehicle_id)

        await self.session.delete(vehicle)
        await self.session.commit()
