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

import enum
from sqlalchemy import Boolean, Column, Integer, Enum, ForeignKey, Float, DateTime

from app.database.base import Base


class FuelType(enum.Enum):
    PETROL_92 = 1
    PETROL_95 = 2
    PETROL_98 = 3
    PETROL_100 = 4
    DIESEL = 5
    GAS = 6
    ELECTRICITY = 7


class FuelModel(Base):
    __tablename__ = "fuels"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    fuel_type = Column(Enum(FuelType), default=FuelType.PETROL_95)
    geo_id = Column(Integer, ForeignKey("geos.id"), nullable=False)
    is_full = Column(Boolean, default=False)
    datetime = Column(DateTime)
