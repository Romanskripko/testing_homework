from typing import Callable

import pytest
from mimesis import Address, Gender, Generic, Person
from mimesis.locales import Locale
from pydantic import BaseModel

from server.apps.identity.models import User


@pytest.fixture()
def user_data_generate() -> BaseModel:
    """Generate user random data and return BaseModel object."""
    generic = Generic(Locale.RU)
    person = Person(Locale.RU)

    class UserDataGenerate(BaseModel):
        first_name: str = person.name()
        last_name: str = person.last_name()
        date_of_birth: str = generic.datetime.date().strftime('%Y-%m-%d')
        address: str = Address(Locale.RU).city()
        job_title: str = person.title()
        email: str = person.email()
        phone: str = person.telephone()
        # static password for auth user
        password1: str = 'password'
        password2: str = 'password'

    return UserDataGenerate()


@pytest.fixture()
def assert_create_correct_user_data() -> Callable[[str, BaseModel], None]:
    """Compare received new user data and data from database."""

    def factory(email: str, register_user_data: BaseModel) -> None:
        user = User.objects.get(email=email)
        assert user.id
        assert user.is_active
        assert not user.is_superuser
        assert not user.is_staff

        for field_name, data_value in register_user_data.model_dump().items():
            if field_name == 'date_of_birth':
                # type date -> str
                assert getattr(user, field_name).strftime('%Y-%m-%d') == data_value
                continue
            if field_name.startswith('password'):
                # skip password fields
                continue
            assert getattr(user, field_name) == data_value

    return factory


@pytest.fixture()
def test_new_user(
    user_data_generate: BaseModel
) -> User:
    """Create new user for testing needs."""
    user_data = user_data_generate.model_dump()
    # sorry for that
    keys_list = ['password1', 'password2']
    [user_data.pop(key) for key in keys_list]
    user = User.objects.create_user(**user_data, password='password')
    return user
