from django.contrib import admin
from .models import (
    Color,
    Shape,
    Program,
    ConfigurationItem,
    ConfigurationItemUpload,
    GroupWbs,
    ProgramUser,
    WbsElement,
    WbsElementUser,
    Sector,
    MaterialMaster,
    MaterialMasterUpload,
    InventoryItem,
    InventoryUpload,
    AltSub,
    AltSubUpload,
)

admin.site.register(Color)
admin.site.register(Shape)


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ["name", "model_code", "id"]
    list_filter = ["name"]


@admin.register(ProgramUser)
class ProgramUserAdmin(admin.ModelAdmin):
    list_display = ["user", "program", "id"]
    list_filter = ["user"]


@admin.register(GroupWbs)
class GroupWbsAdmin(admin.ModelAdmin):
    list_display = ["name", "program_type", "program", "id"]
    list_filter = ["name"]


@admin.register(WbsElement)
class WbsElementAdmin(admin.ModelAdmin):
    list_display = ["group_wbs", "name", "id"]

    class WbsElementUserInline(admin.TabularInline):
        model = WbsElementUser
        extra = 0

    inlines = [WbsElementUserInline]


@admin.register(ConfigurationItem)
class ConfigurationItemAdmin(admin.ModelAdmin):
    list_display = ["name", "req_qty", "req_date", "nomenclature", "configuration_type", "id"]
    list_filter = ["configuration_type"]


@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = ["name", "id"]
    list_filter = ["name"]


@admin.register(MaterialMaster)
class MaterialMasterAdmin(admin.ModelAdmin):
    list_display = ["name", "nomenclature", "upload_id", "id"]
    list_filter = ["name"]


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = [
        "material_master",
        "plant",
        "storage_location",
        "material_type",
        "wbs",
        "shelf_life_expiration_date",
        "upload_id",
        "program_group_wbs",
        "id",
    ]
    list_filter = ["wbs", "material_type", "upload_id"]


@admin.register(AltSub)
class AltSubAdmin(admin.ModelAdmin):
    list_display = ["plant", "model", "type_code", "primary_material", "replacement_part", "created_date", "upload_id", "id"]
    list_filter = ["plant", "model", "type_code"]


admin.site.register(WbsElementUser)
admin.site.register(ConfigurationItemUpload)
admin.site.register(MaterialMasterUpload)
admin.site.register(InventoryUpload)
admin.site.register(AltSubUpload)
