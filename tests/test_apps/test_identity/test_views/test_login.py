from http import HTTPStatus
from typing import Any, Callable, Iterator

import pytest
from django.test import Client
from django.urls import reverse
from pydantic import BaseModel


@pytest.mark.django_db()
def test_registration_get(client: Client) -> None:
    """Basic `get` method for registration page works."""
    response = client.get(reverse('identity:registration'))
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db()
def test_logout_page_get(admin_client: Client) -> None:
    """Basic `get` method for logout page works for authenticated user."""
    response = admin_client.get(reverse('identity:logout'))

    assert response.status_code == HTTPStatus.FOUND


@pytest.mark.django_db()
def test_registration_post(
    client: Client,
    user_data_generate: BaseModel,
    external_api_post_mock: Iterator[dict[str, Any]],
    assert_create_correct_user_data: Callable[[str, BaseModel], None],
) -> None:
    """Test basic user create flow via registration page, mocking external placeholder api."""
    response = client.post(reverse('identity:registration'), data=user_data_generate.model_dump())

    assert response.status_code == HTTPStatus.FOUND

    assert_create_correct_user_data(user_data_generate.email, user_data_generate)  # type: ignore[attr-defined]
