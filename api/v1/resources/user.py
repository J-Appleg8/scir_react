from rest_framework import serializers
from api.viewsets import ProjectionsAndFilters
from django.contrib.auth import get_user_model
User = get_user_model()

class Serializers:
    class Summary(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = [
                'id',
                'get_full_name',
            ]

    class Detail(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = [
                'id',
                'username',
                'first_name',
                'last_name',
                'get_full_name',
            ]

    for_ = {
        'summary': Summary,
        'detail': Detail,
    }

class Viewset(ProjectionsAndFilters):
    serializer_class = Serializers.Summary
    serializers = Serializers
    queryset = User.objects.all()
    ordering_fields = ['id', 'username', 'first_name', 'last_name', 'email',]

    filters = {
        'firstName': lambda q,v,_: q.filter(first_name__icontains=v),
        'lastName': lambda q,v,_: q.filter(last_name__icontains=v),
    }
