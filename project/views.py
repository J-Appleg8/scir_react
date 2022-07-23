from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework import serializers
from django.contrib.auth.models import Group, Permission
from users import models as user_models
from core import models as core_models

from django.contrib.auth import get_user_model

User = get_user_model()


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = "__all__"


class GroupSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True)

    class Meta:
        model = Group
        fields = "__all__"


class CurrentUserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, instance):
        return instance.get_full_name()

    groups = GroupSerializer(many=True)

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "full_name",
            "groups",
        ]


def get_serialized_current_user(request):
    return CurrentUserSerializer(request.user).data if request.user.is_authenticated else None


####################################################################################################
@login_required
def programs(request, *args, **kwargs):
    positions = [{"id": value, "label": label} for value, label in user_models.User.PositionChoices.choices]
    configuration_types = [{"id": value, "label": label} for value, label in core_models.ConfigurationItem.ConfigurationItemTypeChoices.choices]
    return render(
        request,
        "programs.html",
        {"current_user": get_serialized_current_user(request), "positions": positions, "configuration_types": configuration_types},
    )


@login_required
def company_data(request, *args, **kwargs):
    material_types = [{"id": value, "label": label} for value, label in core_models.MaterialMaster.MaterialMasterTypeChoices.choices]
    inventory_types = [{"id": value, "label": label} for value, label in core_models.InventoryItem.InventoryTypeChoices.choices]
    return render(
        request,
        "company_data.html",
        {"current_user": get_serialized_current_user(request), "material_types": material_types, "inventory_types": inventory_types},
    )


####################################################################################################
@login_required
def colors(request, *args, **kwargs):
    return render(request, "colors.html", {"current_user": get_serialized_current_user(request)})


def shapes(request, *args, **kwargs):
    return render(request, "shapes.html", {"current_user": get_serialized_current_user(request)})


@login_required
def active_directory(request, *args, **kwargs):
    return render(request, "active_directory.html", {"current_user": get_serialized_current_user(request)})
