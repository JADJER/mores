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

from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship

from app.database.base import Base
from app.models.domain.profile import Gender


class ProfileModel(Base):
    __tablename__ = "profile"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    username = Column(String, unique=True)
    first_name = Column(String, nullable=True)
    second_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    gender = Column(Enum(Gender), default=Gender.UNDEFINED)
    age = Column(Integer, nullable=True)
    phone = Column(String, unique=True, nullable=True)
    image = Column(String, nullable=True)

    user = relationship("UserModel", back_populates="profile", uselist=False)