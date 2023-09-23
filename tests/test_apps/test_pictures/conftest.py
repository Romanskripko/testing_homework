import json
from typing import Iterator, Callable

import httpretty
import pytest
import requests

from server.apps.pictures.intrastructure.services.placeholder import PictureResponse
from server.settings.components import placeholder


@pytest.fixture()
def assert_correct_pictures() -> Callable[[list[PictureResponse]], None]:
    """Assert pictures."""
    def factory(content: list[PictureResponse]) -> None:
        for picture in content:
            assert isinstance(picture, PictureResponse)

    return factory


@pytest.fixture()
def json_server_photos() -> list[dict[str, str | int]]:
    """Get photos from json_server."""
    return requests.get(
        'http://127.0.0.1:3000/photos',  # wtf
        timeout=1,
    ).json()


@pytest.fixture()
def json_server_photos_to_pydantic(
    json_server_photos: list[dict[str, str | int]]
) -> list[PictureResponse]:
    """Get photos from json_server."""
    return [PictureResponse.model_validate(pic) for pic in json_server_photos]


@pytest.fixture()
def mock_pictures_fetch_api(
    json_server_photos: list[PictureResponse],
) -> Iterator[None]:
    """Route placeholder API endpoint to json-server."""

    with httpretty.httprettized(verbose=True, allow_net_connect=True):
        httpretty.register_uri(
            httpretty.GET,
            uri=f'{placeholder.PLACEHOLDER_API_URL}photos',
            body=json.dumps(json_server_photos),
            content_type='application/json',
        )
        yield
        assert httpretty.has_request()
