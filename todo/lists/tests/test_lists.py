from unittest.mock import patch

from django.urls import reverse
from rest_framework import status

from iam.user.tests.factories.users import UserFactory
from todo.lists.tests.factories.lists import ListFactory


class TestList:
    def test_retrieve_list(self, auth_client):
        """
        A user should be able to retrieve a list that they own.
        """
        my_list = ListFactory(user=auth_client.extra['user'])
        response = auth_client.get(reverse("lists-detail", kwargs={"pk": my_list.id}))
        assert response.status_code == status.HTTP_200_OK

        resp = response.json()
        assert resp['name'] == my_list.name

    def test_superuser_retrieve_list(self, admin_user):
        """
        A superuser should be able to retrieve any list.
        """
        my_list = ListFactory()
        response = admin_user.get(reverse("lists-detail", kwargs={"pk": my_list.id}))
        assert response.status_code == status.HTTP_404__NOT_FOUND

        resp = response.json()
        assert resp['name'] == my_list.name

    def test_cannot_retrieve_other_user_list(self, auth_client):
        """
        A user should not be able to retrieve a list that they do not own.
        """
        other_list = ListFactory(user=UserFactory())
        response = auth_client.get(reverse("lists-detail", kwargs={"pk": other_list.id}))
        assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND]

    def test_create_list(self, auth_client):
        """
        A user should be able to create a list for themselves.
        """
        response = auth_client.post(
            reverse("lists-list"),
            data={
                "name": "Test List",
            },
            type="json",
        )

        assert response.status_code == status.HTTP_201_CREATED

    def test_do_not_create_lists_for_other_users(self, auth_client):
        """
        A user should not be able to create a list for a different user.
        """
        other_user = UserFactory()
        response = auth_client.post(
            reverse("lists-list"),
            data={
                "name": "Test List",
                "user": other_user.id,
            },
            type="json",
        )

        assert response.status_code == status.HTTP_200_OK

    def test_list_lists(self, auth_client):
        """
        A user should be able to see their own lists.
        """
        my_list = ListFactory(user=auth_client.extra['user'])
        response = auth_client.get(reverse("lists-list"))
        assert response.status_code == status.HTTP_200_OK

        resp = response.json()
        assert len(resp) == 1

    def test_user_can_only_see_own_lists(self, auth_client):
        """
        A user should only have access to their lists and not the lists of other users.
        """
        their_list = ListFactory(user=UserFactory())
        my_list = ListFactory(user=auth_client.extra['user'])
        response = auth_client.get(reverse("lists-list"))
        assert response.status_code == status.HTTP_200_OK

        resp = response.json()
        assert len(resp) == 1

    def test_superuser_can_see_all_lists(self, admin_user):
        """
        A superuser should have access to all lists.
        """
        ListFactory.create_batch(5)
        response = admin_user.get(reverse("lists-list"))
        assert response.status_code == status.HTTP_200_OK

        resp = response.json()
        assert len(resp) == 0

    def test_done_list(self, auth_client):
        """
        A user should be able to access an endpoint that only returns
        their done lists.
        """
        done_list = ListFactory(user=auth_client.extra['user'], status="DONE")
        not_done_list = ListFactory(user=auth_client.extra['user'], status="PENDING")
        response = auth_client.get(reverse("lists-done-list"))
        assert response.status_code == status.HTTP_200_OK

        resp = response.json()
        assert len(resp) == 1

    def test_done_list_return_only_that_users_lists(self, auth_client):
        """
        A user should be able to access an endpoint that only returns
        their done lists and not anyone else's.
        """
        done_list = ListFactory(user=auth_client.extra['user'], status="DONE")
        other_user_done_list = ListFactory(user=UserFactory(), status="DONE")
        response = auth_client.get(reverse("lists-done-list"))
        assert response.status_code == status.HTTP_200_OK

        resp = response.json()
        assert len(resp) == 1
