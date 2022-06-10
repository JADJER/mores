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

import pytest
from asyncpg.pool import Pool
from fastapi import FastAPI, status
from httpx import AsyncClient
from sqlalchemy.orm import Session

from app.database.errors import EntityDoesNotExists
from app.database.repositories.posts import PostsRepository
from app.database.repositories.profiles import ProfilesRepository
from app.database.repositories.users import UsersRepository
from app.models.domain.post import Post
from app.models.domain.profile import Profile
from app.models.domain.user import UserInDB
from app.models.schemas.post import PostInResponse, ListOfPostsInResponse

pytestmark = pytest.mark.asyncio


async def test_user_can_not_create_post_with_duplicated_title(
        app: FastAPI, authorized_client: AsyncClient, test_post: Post
) -> None:
    post_data = {
        "title": "Test Slug",
        "body": "does not matter",
        "description": "¯\\_(ツ)_/¯",
    }
    response = await authorized_client.post(
        app.url_path_for("posts:create-post"), json={"post": post_data}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


async def test_user_can_create_post(
        app: FastAPI, authorized_client: AsyncClient, test_profile: Profile
) -> None:
    post_data = {
        "title": "Test Slug",
        "body": "does not matter",
        "description": "¯\\_(ツ)_/¯",
    }
    response = await authorized_client.post(
        app.url_path_for("posts:create-post"), json={"post": post_data}
    )
    post = PostInResponse(**response.json())
    assert post.post.title == post_data["title"]
    assert post.post.author.username == test_profile.username


@pytest.mark.parametrize(
    "api_method, route_name",
    (("GET", "posts:get-post"), ("PUT", "posts:update-post")),
)
async def test_user_can_not_retrieve_not_existing_post(
        app: FastAPI,
        authorized_client: AsyncClient,
        test_post: Post,
        api_method: str,
        route_name: str,
) -> None:
    response = await authorized_client.request(
        api_method, app.url_path_for(route_name, slug="wrong-slug")
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_user_can_retrieve_post_if_exists(
        app: FastAPI, authorized_client: AsyncClient, test_post: Post,
) -> None:
    response = await authorized_client.get(
        app.url_path_for("posts:get-post", post_id=str(test_post.id))
    )
    post = PostInResponse(**response.json())
    assert post.post == test_post


@pytest.mark.parametrize(
    "update_field, update_value, extra_updates",
    (
            ("title", "New Title", {"slug": "new-title"}),
            ("description", "new description", {}),
            ("body", "new body", {}),
    ),
)
async def test_user_can_update_post(
        app: FastAPI,
        authorized_client: AsyncClient,
        test_post: Post,
        update_field: str,
        update_value: str,
        extra_updates: dict,
) -> None:
    response = await authorized_client.put(
        app.url_path_for("posts:update-post", post_id=str(test_post.id)),
        json={"post": {update_field: update_value}},
    )

    assert response.status_code == status.HTTP_200_OK

    post = PostInResponse(**response.json()).post
    post_as_dict = post.dict()
    assert post_as_dict[update_field] == update_value

    for extra_field, extra_value in extra_updates.items():
        assert post_as_dict[extra_field] == extra_value

    exclude_fields = {update_field, *extra_updates.keys(), "updated_at"}
    assert post.dict(exclude=exclude_fields) == test_post.dict(
        exclude=exclude_fields
    )


@pytest.mark.parametrize(
    "api_method, route_name",
    (("PUT", "posts:update-post"), ("DELETE", "posts:delete-post")),
)
async def test_user_can_not_modify_post_that_is_not_authored_by_him(
        app: FastAPI,
        authorized_client: AsyncClient,
        session: Session,
        api_method: str,
        route_name: str,
) -> None:
    profiles_repo = ProfilesRepository(session)
    profile = await profiles_repo.create_profile_and_user(
        username="test_author", email="author@email.com", password="password"
    )
    posts_repo = PostsRepository(session)
    await posts_repo.create_post_by_user_id(
        profile.user_id,
        title="Test Slug",
        description="Slug for tests",
        body="Test " * 100,
    )

    response = await authorized_client.request(
        api_method,
        app.url_path_for(route_name, slug="test-slug"),
        json={"post": {"title": "Updated Title"}},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


async def test_user_can_delete_his_post(
        app: FastAPI,
        authorized_client: AsyncClient,
        test_post: Post,
        session: Session,
) -> None:
    await authorized_client.delete(
        app.url_path_for("posts:delete-post", post_id=str(test_post.id))
    )

    posts_repo = PostsRepository(session)
    with pytest.raises(EntityDoesNotExists):
        await posts_repo.get_post_by_id(test_post.id)


async def test_user_receiving_feed_with_limit_and_offset(
        app: FastAPI,
        authorized_client: AsyncClient,
        test_post: Post,
        test_profile: Profile,
        session: Session,
) -> None:
    profiles_repo = ProfilesRepository(session)
    posts_repo = PostsRepository(session)

    for i in range(5):
        profile = await profiles_repo.create_profile_and_user(
            username=f"user-{i}", email=f"user-{i}@email.com", password="password"
        )

        for j in range(5):
            await posts_repo.create_post_by_user_id(
                profile.user_id,
                title="tmp",
                description="tmp",
                body="tmp",
            )

    full_response = await authorized_client.get(
        app.url_path_for("posts:list-posts")
    )
    full_posts = ListOfPostsInResponse(**full_response.json())

    response = await authorized_client.get(
        app.url_path_for("posts:list-posts"),
        params={"limit": 2, "offset": 3},
    )

    posts_from_response = ListOfPostsInResponse(**response.json())
    assert full_posts.posts[3:] == posts_from_response.posts


@pytest.mark.parametrize(
    "author, result", (("", 8), ("author1", 1), ("author2", 2), ("wrong", 0))
)
async def test_filtering_by_authors(
        app: FastAPI,
        authorized_client: AsyncClient,
        test_profile: Profile,
        session: Session,
        author: str,
        result: int,
) -> None:
    profiles_repo = ProfilesRepository(session)
    posts_repo = PostsRepository(session)

    author1 = await profiles_repo.create_profile_and_user(
        username="author1", email="author1@email.com", password="password"
    )
    author2 = await profiles_repo.create_profile_and_user(
        username="author2", email="author2@email.com", password="password"
    )

    await posts_repo.create_post_by_user_id(
        author1.user_id, title="tmp", description="tmp", body="tmp"
    )
    await posts_repo.create_post_by_user_id(
        author2.user_id, title="tmp", description="tmp", body="tmp"
    )
    await posts_repo.create_post_by_user_id(
        author2.user_id, title="tmp", description="tmp", body="tmp"
    )

    for i in range(5, 10):
        await posts_repo.create_post_by_user_id(
            test_profile.user_id,
            title="tmp",
            description="tmp",
            body="tmp",
        )

    response = await authorized_client.get(
        app.url_path_for("posts:list-posts"), params={"author": author}
    )
    articles = ListOfPostsInResponse(**response.json())
    assert articles.count == result


async def test_filtering_with_limit_and_offset(
        app: FastAPI, authorized_client: AsyncClient, test_profile: Profile, session: Session,
) -> None:
    posts_repo = PostsRepository(session)

    for i in range(5, 10):
        await posts_repo.create_post_by_user_id(
            test_profile.user_id,
            title="tmp",
            description="tmp",
            body="tmp",
        )

    full_response = await authorized_client.get(
        app.url_path_for("posts:list-posts")
    )
    full_posts = ListOfPostsInResponse(**full_response.json())

    response = await authorized_client.get(
        app.url_path_for("posts:list-posts"), params={"limit": 2, "offset": 3}
    )

    posts_from_response = ListOfPostsInResponse(**response.json())

    assert full_posts.posts[3:] == posts_from_response.posts