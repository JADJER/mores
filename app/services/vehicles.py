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

from app.database.errors import EntityDoesNotExists
from app.database.repositories.vehicles import VehiclesRepository


async def check_vehicle_is_exist_by_id_and_user_id(repo: VehiclesRepository, vehicle_id: int, user_id: int) -> bool:
    try:
        await repo.get_vehicle_by_id_and_user_id(vehicle_id, user_id)
    except EntityDoesNotExists:
        return False

    return True


async def check_vin_is_taken(repo: VehiclesRepository, vin: str) -> bool:
    try:
        await repo.get_vehicle_by_vin(vin)
    except EntityDoesNotExists:
        return False

    return True


async def check_registration_plate_is_taken(repo: VehiclesRepository, registration_plate: str) -> bool:
    try:
        await repo.get_vehicle_by_registration_plate(registration_plate)
    except EntityDoesNotExists:
        return False

    return True


async def check_user_is_owner(repo: VehiclesRepository, vehicle_id: int, user_id: int) -> bool:
    return await check_vehicle_is_exist_by_id_and_user_id(repo, vehicle_id, user_id)


async def get_current_mileage_by_vehicle_id(repo: VehiclesRepository, vehicle_id: int, user_id: int) -> int:
    vehicle = await repo.get_vehicle_by_id_and_user_id(vehicle_id, user_id)
    return vehicle.mileage


async def check_mileage_increases(repo: VehiclesRepository, vehicle_id: int, user_id: int, mileage: int) -> bool:
    current_mileage = await get_current_mileage_by_vehicle_id(repo, vehicle_id, user_id)

    if mileage <= current_mileage:
        return False

    return True


async def update_vehicle_mileage(repo: VehiclesRepository, vehicle_id: int, user_id: int, mileage: int) -> bool:
    if not await check_mileage_increases(repo, vehicle_id, user_id, mileage):
        return False

    await repo.update_vehicle_by_id_and_user_id(vehicle_id, user_id, mileage=mileage)

    return True
