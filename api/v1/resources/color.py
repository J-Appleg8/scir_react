import json
from rest_framework import serializers, viewsets
from api.viewsets import ProjectionsAndFilters
from core.models import Color

class Serializers:
    class Summary(serializers.ModelSerializer):
        class Meta:
            model = Color
            fields = [
                'id',
                'name',
                'is_primary',
                'red',
                'green',
                'blue',
            ]

        def create(self, validated_data):
            return super().create(validated_data)

        def update(self, instance, validated_data):
            return super().update(instance, validated_data)

    class Detail(serializers.ModelSerializer):
        class Meta:
            model = Color
            fields = [
                'id',
                'name',
                'is_primary',
                'red',
                'green',
                'blue',
                'hex_code',
            ]

    for_ = {
        'summary': Summary,
        'detail': Detail,
    }

class Viewset(ProjectionsAndFilters):
    serializer_class = Serializers.Summary
    serializers = Serializers
    queryset = Color.objects.all()
    ordering_fields = '__all__'

    filters = {
        'name': lambda q,v,_: q.filter(name__icontains=v),
        'is_primary': lambda q,v,_: q.filter(is_primary=json.loads(v)),
        'red': lambda q,v,_: q.filter(red=v),
        'green': lambda q,v,_: q.filter(green=v),
        'blue': lambda q,v,_: q.filter(blue=v),
    }

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

