import pytest
from django.urls import reverse
from rest_framework import status

from todo.items.tests.factories.items import ItemFactory
from todo.lists.models import List
from todo.lists.tests.factories.lists import ListFactory


class TestListItems:
    def test_create_list_item(self, auth_client):
        """
        A user should be able to create a list item for themselves.
        """
        my_list = ListFactory(user=auth_client.extra['user'])
        response = auth_client.post(
            reverse("items-list"),
            data={
                "name": "Test Item",
                "content": "Test Item Content",
                "list": my_list.id,
            },
            type="json",
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_mark_list_item_as_done(self, auth_client):
        """
        A user should be able to mark a list item as done.
        """
        my_list = ListFactory(user=auth_client.extra['user'])
        my_item = ItemFactory(list=my_list, status="PENDING")
        response = auth_client.patch(
            reverse("items-detail", kwargs={"pk": my_item.id}),
            data={
                "status": "DONE",
            },
            type="json",
        )

        assert response.status_code == status.HTTP_200_OK

        resp = response.json()
        assert resp['status'] == "DONE"
