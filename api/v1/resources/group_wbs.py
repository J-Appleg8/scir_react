from rest_framework import serializers
from core.models import GroupWbs
from api.viewsets import ProjectionsAndFilters


class Serializers:
    class Summary(serializers.ModelSerializer):
        class Meta:
            model = GroupWbs
            fields = [
                "id",
                "name",
            ]

    class Detail(serializers.ModelSerializer):
        class Meta:
            model = GroupWbs
            fields = [
                "id",
                "name",
                "program",
                "program_type",
            ]

        chain_queryset = lambda q, r: q.select_related("program")

    for_ = {
        "summary": Summary,
        "detail": Detail,
    }


class Viewset(ProjectionsAndFilters):
    queryset = GroupWbs.objects.all()
    serializers = Serializers
    serializer_class = Serializers.Summary

    ordering_fileds = ["name"]
    ordering = ["name"]

    filters = {
        "name": lambda q, v, _: q.filter(name__icontains=v),
    }
