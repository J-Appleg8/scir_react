from django.db.models import OuterRef, Value as V, Exists
from rest_framework import serializers
from api.viewsets import ProjectionsAndFilters
from django.contrib.auth import get_user_model
from core.models import ProgramUser
from . import user

User = get_user_model()


class Serializers:
    class Summary(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = [
                "id",
                "username",
            ]

    class ForUserForm(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = [
                "id",
                "get_full_name",
            ]

        def to_representation(self, instance):
            try:
                response = super().to_representation(instance)
                return response
            except Exception as e:
                print(e)

    class Detail(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = [
                "id",
                "username",
                "first_name",
                "last_name",
                "get_full_name",
                "get_position_display",
            ]

        def to_representation(self, instance):
            try:
                response = super().to_representation(instance)
                return response
            except Exception as e:
                print(e)

    for_ = {
        "summary": Summary,
        "detail": Detail,
    }


class Viewset(ProjectionsAndFilters):
    serializer_class = Serializers.Summary
    serializers = Serializers
    queryset = User.objects.all()
    ordering_fields = ["id", "username", "first_name", "last_name", "get_full_name", "get_position_display", "email"]

    filters = {
        "firstName": lambda q, v, _: q.filter(first_name__icontains=v),
        "lastName": lambda q, v, _: q.filter(last_name__icontains=v),
        "username": lambda q, v, _: q.filter(username__icontains=v),
        # OuterRef is referring to the outer query when in a subquery
        # example below: OuterRef is used in the ProgramUser filter statement to refer to the User 'id' (outer query)
        "available_for_programs": lambda q, v, _: User.objects.filter(
            ~Exists(
                ProgramUser.objects.filter(user=OuterRef("id")).filter(program=v),
            )
        ),
    }
