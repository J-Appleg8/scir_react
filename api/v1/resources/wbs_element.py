from telnetlib import DET
from django.db.models import Prefetch
from rest_framework import serializers
from core.models import ConfigurationItem, WbsElement
from api.viewsets import ProjectionsAndFilters


class Serializers:
    class Summary(serializers.ModelSerializer):
        class Meta:
            model = WbsElement
            fields = [
                "id",
                "name",
            ]

    class Detail(serializers.ModelSerializer):
        class Meta:
            model = WbsElement
            fields = [
                "id",
                "name",
                "configuration_items",
            ]

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            from . import configuration_item

            self.fields["configuration_items"] = configuration_item.Serializers.WithWbsElement(many=True)

    for_ = {
        "summary": Summary,
        "detail": Detail,
    }


class Viewset(ProjectionsAndFilters):
    queryset = WbsElement.objects.prefetch_related(Prefetch(lookup="configuration_items", queryset=ConfigurationItem.objects.prefetch_related("parents")))
    serializers = Serializers
    serializer_class = Serializers.Detail

    filters = {
        "name": lambda q, v, _: q.filter(name=v),
    }
