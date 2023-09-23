import json
import re
from http import HTTPStatus
from typing import Any, Iterator

import httpretty
import pytest
from mimesis import Generic
from pydantic import BaseModel

from server.settings.components import placeholder


@pytest.fixture()
def external_api_placeholder_lead_id_response(
    user_data_generate: BaseModel
) -> dict[str, Any]:
    """Return external_placeholder_lead_id_response."""
    response_model_dict = user_data_generate.model_dump()
    response_model_dict['id'] = Generic().code.random.randint(1, 999)

    return response_model_dict


@pytest.fixture()
def external_api_post_mock(
    external_api_placeholder_lead_id_response: Iterator[dict[str, Any]]
) -> Iterator[dict[str, Any]]:
    """Mock external API request for user creation."""
    with httpretty.httprettized(verbose=True, allow_net_connect=True):
        httpretty.register_uri(
            method=httpretty.POST,
            uri=f'{placeholder.PLACEHOLDER_API_URL}users',
            body=json.dumps(external_api_placeholder_lead_id_response),
            status=HTTPStatus.CREATED
        )
        yield external_api_placeholder_lead_id_response  # type: ignore[misc]

        assert httpretty.has_request()


@pytest.fixture()
def external_api_patch_mock(
    external_api_placeholder_lead_id_response: Iterator[dict[str, Any]]
) -> Iterator[dict[str, Any]]:
    """Mock external API request for user update."""
    with httpretty.httprettized(verbose=True, allow_net_connect=True):
        httpretty.register_uri(
            method=httpretty.PATCH,
            uri=re.compile(f'{placeholder.PLACEHOLDER_API_URL}users/.*'),
            body=json.dumps(external_api_placeholder_lead_id_response),
            status=HTTPStatus.OK
        )
        yield external_api_placeholder_lead_id_response  # type: ignore[misc]

        assert httpretty.has_request()
