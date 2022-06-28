from rest_framework import serializers
from api.viewsets import ProjectionsAndFilters
from core.models import Shape

class Serializers:
    class Summary(serializers.ModelSerializer):
        class Meta:
            model = Shape
            fields = [
                'id',
                'name',
            ]

    for_ = {
        'summary': Summary,
    }

class Viewset(ProjectionsAndFilters):
    serializer_class = Serializers.Summary
    serializers = Serializers
    queryset = Shape.objects.all()
    ordering_fields = ['id', 'name']

    filters = {
        'name': lambda q,v,_: q.filter(name__icontains=v),
    }

