from http import HTTPStatus
from typing import Any, Iterator

import pytest
from django.forms import model_to_dict
from django.test import Client
from django.urls import reverse

from server.apps.identity.models import User


@pytest.mark.django_db()
def test_update_exist_user_data_field(
    logged_in_client: Client,
    test_new_user: User,
    external_api_patch_mock: Iterator[dict[str, Any]],
) -> None:
    """Test basic user update flow"""
    new_first_name: str = test_new_user.first_name[::-1]
    update_data: dict[str, Any] = model_to_dict(
        test_new_user, fields=User.REQUIRED_FIELDS,
    )
    update_data['first_name'] = new_first_name

    resp = logged_in_client.post(reverse('identity:user_update'), data=update_data)

    assert resp.status_code == HTTPStatus.FOUND
    user = User.objects.get(id=test_new_user.id)
    assert user.first_name == new_first_name
