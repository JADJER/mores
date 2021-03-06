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

from enum import Enum

from app.models.domain.rwmodel import RWModel
from app.models.domain.user import User


class EventConfirmationType(Enum):
    YES = "yes"
    MAY_BE_YES = "may_be_yes"
    MAY_BY = "may_be"
    MAY_BE_NO = "may_be_no"
    NO = "no"


class EventConfirmation(RWModel):
    user: User
    confirm_type: EventConfirmationType
