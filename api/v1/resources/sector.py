from django.contrib.auth import get_user_model
from rest_framework import serializers
from api.viewsets import ProjectionsAndFilters
from core.models import Sector

User = get_user_model()


class Serializers:
    class Summary(serializers.ModelSerializer):
        class Meta:
            model = Sector
            fields = [
                "id",
                "name",
            ]

    for_ = {
        "summary": Summary,
    }


class Viewset(ProjectionsAndFilters):
    queryset = Sector.objects.all()
    serializer_class = Serializers.Summary
    serializers = Serializers

    filters = {
        "name": lambda q, v, _: q.filter(name=v),
    }
