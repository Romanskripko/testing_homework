from http import HTTPStatus
from typing import Callable

import pytest
from django.test import Client
from django.urls import reverse

from server.apps.pictures.intrastructure.services.placeholder import PictureResponse


@pytest.mark.slow()
@pytest.mark.django_db()
def test_view_pictures_full(
    logged_in_client: Client,
    assert_correct_pictures: Callable[[list[PictureResponse]], None]
) -> None:
    """Test basic pictures view running actual http request to placeholder api."""
    resp = logged_in_client.get(reverse('pictures:dashboard'))

    assert resp.status_code == HTTPStatus.OK
    assert_correct_pictures(resp.context['pictures'])


@pytest.mark.django_db()
def test_view_pictures_json_webserver(
    logged_in_client: Client,
    mock_pictures_fetch_api: dict[str, int | str],
    json_server_photos_to_pydantic: list[PictureResponse],
    assert_correct_pictures: Callable[[list[PictureResponse]], None]
) -> None:
    """Test pictures view running request to json webserver instead of placeholder api"""
    resp = logged_in_client.get(reverse('pictures:dashboard'))

    assert resp.status_code == HTTPStatus.OK
    assert_correct_pictures(resp.context['pictures'])
    assert len(resp.context['pictures']) == len(json_server_photos_to_pydantic)
    assert resp.context['pictures'] == json_server_photos_to_pydantic
