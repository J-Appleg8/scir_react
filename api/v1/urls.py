from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from .resources import (
    alt_sub,
    alt_sub_upload,
    configuration_item,
    configuration_item_upload,
    wbs_element,
    group_wbs,
    material_master,
    material_master_upload,
    inventory_item,
    inventory_item_upload,
    program,
    program_user,
    sector,
    user,
    color,
    shape,
)

router = DefaultRouter()

router.register("users", user.Viewset)
router.register("colors", color.Viewset)
router.register("shapes", shape.Viewset)
# Programs
router.register("programs", program.Viewset)
router.register("program_users", program_user.Viewset)
router.register("group_wbss", group_wbs.Viewset)
router.register("wbs_elements", wbs_element.Viewset)
router.register("configuration_items", configuration_item.Viewset)
router.register("configuration_item_uploads", configuration_item_upload.Viewset)
# Company Data
router.register("sectors", sector.Viewset)
router.register("material_masters", material_master.Viewset)
router.register("material_master_uploads", material_master_upload.Viewset)
router.register("inventory_items", inventory_item.Viewset)
router.register("inventory_item_uploads", inventory_item_upload.Viewset)
router.register("alt_subs", alt_sub.Viewset)
router.register("alt_sub_uploads", alt_sub_upload.Viewset)

urlpatterns = [
    path("", include(router.urls)),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("schema/swagger_ui", SpectacularSwaggerView.as_view(), name="swagger_ui"),
]
