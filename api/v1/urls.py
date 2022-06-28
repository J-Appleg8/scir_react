from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .resources import (
    user,
    color,
    shape,
)

router = DefaultRouter()

router.register('users', user.Viewset)
router.register('colors', color.Viewset)
router.register('shapes', shape.Viewset)

urlpatterns = [
    path('', include(router.urls)),
]
