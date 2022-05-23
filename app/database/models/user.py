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

from sqlalchemy import Boolean, Column, Integer, String, Enum

from app.database.base import Base
from app.models.domain.user import Gender


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String, unique=True)
    email = Column(String, unique=True)
    phone = Column(String, unique=True)
    password = Column(String)

    first_name = Column(String)
    second_name = Column(String)
    last_name = Column(String)
    gender = Column(Enum(Gender))
    age = Column(Integer)

    is_admin = Column(Boolean, default=False)
    is_blocked = Column(Boolean, default=False)