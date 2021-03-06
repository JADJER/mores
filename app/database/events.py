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

from fastapi import FastAPI
from loguru import logger

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.settings.app import AppSettings


async def connect_to_db(app: FastAPI, settings: AppSettings) -> AsyncSession:
    logger.info("Connecting to Postgres")

    engine = create_async_engine(
        settings.get_database_url,
        echo=True
    )
    app.state.engine = engine

    async_session = sessionmaker(
        bind=engine,
        expire_on_commit=False,
        class_=AsyncSession
    )

    session = async_session()

    app.state.session = session
    logger.info("Connection established")

    return session


async def close_db_connection(app: FastAPI) -> None:
    logger.info("Closing connection to database")

    await app.state.engine.dispose()

    logger.info("Connection closed")
