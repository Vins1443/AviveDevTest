from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from todo.lists.models import List
from todo.lists.permissions import ListPermission
from todo.lists.serializers import ListSerializer, RetrieveListSerializer, CreateListSerializer

from utils.mixins.viewsets.action_serializer_mapping import (  # isort:skip
    ViewSetActionSerializerMixin,  # isort:skip
)


class ListViewSet(viewsets.ModelViewSet, ViewSetActionSerializerMixin):
    queryset = List.objects.all()
    serializer_action_classes = {
        "create": CreateListSerializer,
        "list": ListSerializer,
        "retrieve": RetrieveListSerializer,
        "done_list": ListSerializer,
    }
    permission_classes = [IsAuthenticated, ListPermission]

    def get_serializer_class(self):
        return self.serializer_action_classes.get(self.action, ListSerializer)
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return List.objects.all()
        if user.is_staff:
            return List.objects.all()
        return List.objects.filter(user=user)

    

    @extend_schema(responses={200: CreateListSerializer(many=True)})
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(responses={200: ListSerializer(many=True)})
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(responses={200: RetrieveListSerializer()})
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(responses={200: ListSerializer(many=True)})
    @action(methods=["get"], detail=False)
    def done_list(self, request, *args, **kwargs):
        """
        Returns a user's lists that have a status of DONE.
        """
        serializer = self.get_serializer_class()
        queryset = self.get_queryset().filter(status="DONE")
        data = serializer(queryset, many=True).data
        return Response(data)
