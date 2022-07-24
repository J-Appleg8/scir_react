from rest_framework import serializers
from core.models import AltSub
from api.viewsets import ProjectionsAndFilters


class Serializers:
    class Summary(serializers.ModelSerializer):
        class Meta:
            model = AltSub
            fields = [
                "id",
                "primary_material",
                "replacement_part",
            ]

    class Detail(serializers.ModelSerializer):
        class Meta:
            model = AltSub
            fields = [
                "id",
                "plant",
                "model",
                "type_code",
                "primary_material",
                "replacement_part",
                "next_higher_assembly",
                "alternate_or_substitute_code",
                "sub_code",
                "wbs_element",
                "revision_level",
                "reason_for_change",
                "item_text_line",
                "created_by",
            ]

        chain_queryset = lambda q, r: q.select_related("model").select_related("primary_material").select_related("replacement_part")

    for_ = {
        "summary": Summary,
        "detail": Detail,
    }


class ViewSet(ProjectionsAndFilters):
    queryset = AltSub.objects.all()
    serializers = Serializers
    serializer_class = Serializers.Detail

    ordering = ["primary_material"]

    filters = {
        "plant": lambda q, v, _: q.filter(plant_icontains=v),
        "model": lambda q, v, _: q.filter(model_icontains=v),
        "type_code": lambda q, v, _: q.filter(type_code_icontains=v),
        "primary_material": lambda q, v, _: q.filter(primary_material__name__icontains=v),
        "replacement_part": lambda q, v, _: q.filter(replacement_part__name__icontains=v),
    }
