from rest_framework import serializers
from core.models import Program
from . import user, group_wbs, program_user
from api.viewsets import ProjectionsAndFilters
from django.contrib.auth import get_user_model

User = get_user_model()


class Serializers:
    class Summary(serializers.ModelSerializer):
        class Meta:
            model = Program
            fields = [
                "id",
                "name",
                "model_code",
            ]

    # ################################################################################
    class Detail(serializers.ModelSerializer):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields["users"] = user.Serializers.Detail(many=True)
            self.fields["group_wbs_set"] = group_wbs.Serializers.Detail(many=True)

        class Meta:
            model = Program
            fields = [
                "id",
                "name",
                "group_wbs_set",
                "users",
                "model_code",
            ]

        chain_queryset = lambda q, r: q.prefetch_related("group_wbs_set").prefetch_related("users")

    # ################################################################################
    class Edit(serializers.ModelSerializer):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields["program_users"] = program_user.Serializers.Detail(many=True)
            self.fields["group_wbs_set"] = group_wbs.Serializers.Summary(many=True)

        class Meta:
            model = Program
            fields = [
                "id",
                "name",
                "group_wbs_set",
                "program_users",
                "model_code",
            ]

        chain_queryset = lambda q, r: q.prefetch_related("group_wbs_set").prefetch_related("program_users")

    # ################################################################################
    class Create(serializers.ModelSerializer):
        class Meta:
            model = Program
            fields = [
                "id",
                "name",
                "model_code",
            ]

    for_ = {
        "summary": Summary,
        "detail": Detail,
        "POST": Create,
        "edit": Edit,
        "PUT": Edit,
        "PATCH": Edit,
    }


class Viewset(ProjectionsAndFilters):
    queryset = Program.objects.all()
    serializers = Serializers
    serializer_class = Serializers.Summary

    ordering_fileds = ["name", "model_code", "group_wbs_set__name"]
    ordering = ["name"]

    filters = {
        "name": lambda q, v, _: q.filter(name__icontains=v),
        "model_code": lambda q, v, _: q.filter(model_code__icontains=v),
        "group_wbs": lambda q, v, _: q.filter(group_wbs_set__name__icontains=v),
    }
