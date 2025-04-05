import pytest

from rest_framework.test import APIClient

from iam.user.tests.factories.users import UserFactory


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture
def auth_client(request):
    if request.node.get_closest_marker('username'):
        user = UserFactory(username=request.node.get_closest_marker('username').args[0])
    else:
        user = UserFactory()

    client = APIClient()
    client.force_authenticate(user=user)
    client.extra = {'user': user}
    yield client


@pytest.fixture
def admin_user(request):
    if request.node.get_closest_marker('username'):
        user = UserFactory(
            username=request.node.get_closest_marker('username').args[0],
            is_staff=True,
            is_superuser=True
        )
    else:
        user = UserFactory(is_staff=True, is_superuser=True)

    client = APIClient()
    client.force_authenticate(user=user)
    client.extra = {'user': user}
    yield client
