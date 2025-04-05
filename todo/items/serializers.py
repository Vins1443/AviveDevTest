from rest_framework import serializers

from todo.items.models import Item
from todo.lists.models import List


class ItemSerializer(serializers.ModelSerializer):
    list = serializers.PrimaryKeyRelatedField(queryset=List.objects.all())

    class Meta:
        model = Item
        fields = (
            "id",
            "name",
            "content",
            "list",
            "status",
            "created_at",
            "updated_at",
            "deadline",
        )
