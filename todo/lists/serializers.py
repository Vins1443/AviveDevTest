from django.contrib.auth import get_user_model
from rest_framework import serializers

from iam.user.serializers import UserSerializer
from todo.items.serializers import ItemSerializer
from todo.lists.models import List

User = get_user_model()


class CreateListSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        default=serializers.CurrentUserDefault(), queryset=User.objects.all()
    )

    class Meta:
        model = List
        fields = ["name", "user", "status", "created_at", "updated_at", "deadline", "completed_at"]

    def validate_user(self, value):
        if self.context["request"].user != value:
            raise serializers.ValidationError("cannot create list for another user") 
        return value   


class ListSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        default=serializers.CurrentUserDefault(), queryset=User.objects.all()
    )

    class Meta:
        model = List
        fields = ["name", "user", "status", "created_at", "updated_at", "deadline", "completed_at"]


class RetrieveListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    items = ItemSerializer(many=True)

    class Meta:
        model = List
        fields = [
            "name",
            "user",
            "status",
            "created_at",
            "updated_at",
            "items",
            "deadline",
            "completed_at"
        ]
