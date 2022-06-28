from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework import serializers
from django.contrib.auth.models import Group, Permission

from django.contrib.auth import get_user_model
User = get_user_model()

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True)
    class Meta:
        model = Group
        fields = '__all__'

class CurrentUserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    def get_full_name(self, instance):
        return instance.get_full_name()

    groups = GroupSerializer(many=True)

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'full_name',
            'groups',
        ]

def get_serialized_current_user(request):
    return CurrentUserSerializer(request.user).data if request.user.is_authenticated else None

@login_required
def colors(request, *args, **kwargs):
    return render(request, 'colors.html', { 'current_user': get_serialized_current_user(request) })

def shapes(request, *args, **kwargs):
    return render(request, 'shapes.html', { 'current_user': get_serialized_current_user(request) })

@login_required
def active_directory(request, *args, **kwargs):
    return render(request, 'active_directory.html', { 'current_user': get_serialized_current_user(request) })
