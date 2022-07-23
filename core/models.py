from attr import field
from django.conf import settings
from django.db import models
from django.db.models import constraints, Sum
from django.utils.text import slugify
from django.forms import ValidationError
from django.urls import reverse
from django.core.validators import RegexValidator
import datetime
from functools import cached_property
from django.core.validators import MinValueValidator, MaxValueValidator


validate_y_group = RegexValidator(regex=r"^[Y]-[A-Z0-9]{5}-[A-Z]{2}$", message="Please enter a valid Y-Group")


def format_to_percent(obj, sigdigits):
    if obj:
        return "{0:.{sigdigits}%}".format(obj, sigdigits=sigdigits)
    else:
        return obj


class Color(models.Model):
    name = models.CharField(max_length=20)
    is_primary = models.BooleanField(default=False)
    red = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(255)])
    green = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(255)])
    blue = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(255)])

    @cached_property
    def hex_code(self):
        def color_hex_pair(color_value: int) -> str:
            return hex(color_value)[2:].rjust(2, "0")

        r = color_hex_pair(self.red)
        g = color_hex_pair(self.green)
        b = color_hex_pair(self.blue)

        return f"#{r}{g}{b}"

    __str__ = __repr__ = lambda self: self.name


class Shape(models.Model):
    name = models.CharField(max_length=20)

    __str__ = __repr__ = lambda self: self.name


####################################################################################################
# Program Model
class Program(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through="ProgramUser", blank=True, related_name="programs")
    model_code = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(max_length=100, null=True, blank=True)

    class Meta:
        constraints = [constraints.UniqueConstraint(fields=["name"], name="unique_programs")]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    # def get_absolute_url(self):
    #     return reverse("programs:program_index")


class ProgramUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="program_users")
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name="program_users")


####################################################################################################
# Group WBS & WBS Elements Models
class GroupWbs(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name="group_wbs_set")

    class ProgramTypeChoices(models.IntegerChoices):
        DELIVERABLE_FLIGHT = 1, "DF"
        DELIVERABLE_RAPID = 2, "DR"
        DELIVERABLE_ENGINEERING = 3, "DE"
        NON_FLIGHT = 4, "NE"

    program_type = models.IntegerField(choices=ProgramTypeChoices.choices, null=True, verbose_name=" Program Type")
    name = models.CharField(max_length=50, null=True, validators=[validate_y_group])

    def _str__(self):
        return self.name

    class Meta:
        constraints = [constraints.UniqueConstraint(fields=["program", "program_type"], name="unique_group_wbs")]


# MEAC Report should have the WBS Element descriptions
class WbsElement(models.Model):
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, through="WbsElementUser", related_name="wbs_elements")
    group_wbs = models.ForeignKey(GroupWbs, on_delete=models.CASCADE, related_name="wbs_elements")
    name = models.CharField(max_length=100)

    class Meta:
        constraints = [constraints.UniqueConstraint(fields=["group_wbs", "name"], name="unique_wbs_elements")]

    def _str__(self):
        return self.name


class WbsElementUser(models.Model):
    wbs_element = models.ForeignKey(WbsElement, on_delete=models.CASCADE, related_name="wbs_element_users")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wbs_element_users")

    def clean(self):
        if not self.wbs_element.group_wbs.program.users.filter(id=self.user.id).exists():
            raise ValidationError({"user": f"This user is not assigned to {self.wbs_element.group_wbs.program.name}"})


# Configuration Item Models
class ConfigurationItemUpload(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name="configuration_item_uploads")
    data_file = models.FileField(blank=True, null=True, upload_to="program_reports/%Y/%m/%d")
    created = models.DateTimeField(auto_now_add=True)


class ConfigurationItem(models.Model):
    wbs_element = models.ForeignKey(WbsElement, on_delete=models.CASCADE, related_name="configuration_items")
    upload = models.ForeignKey(ConfigurationItemUpload, null=True, on_delete=models.CASCADE, related_name="configuration_items")
    name = models.CharField(max_length=100)
    parents = models.ManyToManyField("self", symmetrical=False, related_name="children")

    class ConfigurationTypeChoices(models.IntegerChoices):
        MAKE = 3, "MAKE"
        MSUB = 4, "MSUB"
        PRCH = 5, "PRCH"

    configuration_type = models.IntegerField(choices=ConfigurationTypeChoices.choices, null=True, verbose_name="Item Type")
    nomenclature = models.CharField(max_length=100, null=True, blank=True)
    req_qty = models.FloatField(null=True)
    req_date = models.DateField(blank=True, null=True)
    net_order = models.CharField(max_length=100)
    replenishment = models.CharField(max_length=100)
    po_delivery = models.DateField(blank=True, null=True)

    class Meta:
        constraints = [
            constraints.UniqueConstraint(
                fields=[
                    "wbs_element",
                    "name",
                    "configuration_type",
                    "net_order",
                    "replenishment",
                ],
                name="unique_configuration_item",
            )
        ]

    def _str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("programs", kwargs={"slug": self.wbs_element.group_wbs.program.slug, "pk": self.pk})

    @property
    def total_parent_items(self):
        return len(self.parents.all())

    @property
    def total_children_items(self):
        return len(self.children.all())

    @property
    def total_parts_in_inventory(self):
        counter = 0
        for child in self.children.all():
            if child.replenishment == "ON-HAND QTY":
                counter += 1
        return counter

    @property
    def calculate_kit_ready_percentage(self):
        if self.total_parts_in_inventory > 0:
            return format_to_percent(self.total_parts_in_inventory / self.total_children_items, 0)
        else:
            return 0.0

    ##############################
    # *Get rid of
    def get_parent_object(self):
        for parent in self.parents.all():
            if parent.replenishment == self.net_order:
                return parent

    parent = property(get_parent_object)

    @property
    def is_late_to_need(self):
        if self.configuration_type == 3:
            return None

        elif self.po_delivery:
            late_flag = self.req_date < self.po_delivery

            if late_flag:
                return "LTN"
        elif self.replenishment == "ON-HAND QTY":
            return "ON TIME"

    ##############################
    # *Get rid of
    @property
    def total_program_inventory(self):
        try:
            inv = (
                InventoryItem.objects.filter(program_group_wbs_id=self.wbs_element.group_wbs_id)
                .filter(material_master_id__name=self.name)
                .aggregate(Sum("on_hand_inventory"))
            )
            return inv["on_hand_inventory__sum"]
        except InventoryItem.DoesNotExist:
            return None

    @property
    def formatted_req_date(self):
        return datetime.date.strftime(self.req_date, "%m/%d/%Y")


####################################################################################################
# Company Data Models
class Sector(models.Model):
    name = models.CharField(max_length=100)


####################################################################################################
# Material Master Models
class MaterialMasterUpload(models.Model):
    sector = models.ForeignKey(Program, on_delete=models.CASCADE, related_name="material_master_uploads")
    data_file = models.FileField(upload_to="material_master_reports/%Y/%m/%d")
    created = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("core:material_master_list")


class MaterialMaster(models.Model):
    name = models.CharField(max_length=100, unique=True)
    nomenclature = models.CharField(max_length=100, null=True, blank=True)
    plant = models.CharField(max_length=100)

    class MaterialMasterTypeChoices(models.IntegerChoices):
        MAKE = 3, "MAKE"
        MSUB = 4, "MSUB"
        PRCH = 5, "PRCH"

    material_type = models.IntegerField(choices=MaterialMasterTypeChoices.choices, null=True, verbose_name="Matl Type")
    base_unit_of_measure = models.CharField(max_length=100)
    procurement_type = models.CharField(max_length=100)
    goods_receipt_time = models.IntegerField(blank=True, null=True)
    planned_delivery_time = models.IntegerField(blank=True, null=True)
    storage_condition = models.CharField(max_length=100, null=True, blank=True)
    base_drawing = models.CharField(max_length=100, null=True, blank=True)
    electrical_flag = models.CharField(max_length=100, null=True, blank=True)
    upload = models.ForeignKey(MaterialMasterUpload, null=True, on_delete=models.CASCADE, related_name="material_master_items")

    def _str__(self):
        return self.name


####################################################################################################
# Inventory Models
class InventoryUpload(models.Model):
    sector = models.ForeignKey(Program, on_delete=models.CASCADE, related_name="inventory_uploads")
    data_file = models.FileField(upload_to="inventory_reports/%Y/%m/%d")
    created = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("core:inventory_list")


class InventoryItem(models.Model):
    material_master = models.ForeignKey(MaterialMaster, to_field="name", on_delete=models.PROTECT, related_name="inventory_items")
    plant = models.CharField(max_length=100)
    storage_location = models.CharField(max_length=100)

    class InventoryTypeChoices(models.IntegerChoices):
        MAKE = 3, "MAKE"
        MSUB = 4, "MSUB"
        PRCH = 5, "PRCH"

    material_type = models.IntegerField(choices=InventoryTypeChoices.choices, null=True, verbose_name="Matl Type")
    wbs = models.CharField(max_length=100, blank=True, null=True)
    batch = models.CharField(max_length=100)
    lot_date_code = models.CharField(max_length=100, blank=True, null=True)
    base_unit_of_measure = models.CharField(max_length=100)
    unrestricted_inventory = models.FloatField(null=True)
    qm_lot_inventory = models.FloatField(null=True)
    restricted_inventory = models.FloatField(null=True)
    blocked_inventory = models.FloatField(null=True)
    shelf_life_expiration_date = models.DateField(blank=True, null=True)
    discard_date = models.DateField(blank=True, null=True)
    on_hand_inventory = models.FloatField(null=True)
    upload = models.ForeignKey(InventoryUpload, null=True, on_delete=models.CASCADE, related_name="inventory_items")
    program_group_wbs = models.ForeignKey(GroupWbs, blank=True, null=True, on_delete=models.CASCADE, related_name="inventory_items")

    def get_absolute_url(self):
        return reverse("core:inventory_list")


####################################################################################################
# Alt/Sub Models
class AltSubUpload(models.Model):
    sector = models.ForeignKey(Program, on_delete=models.CASCADE, related_name="altsub_uploads")
    data_file = models.FileField(upload_to="altsub_reports/%Y/%m/%d")
    created = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("core:altsub_list")


class AltSub(models.Model):
    plant = models.CharField(max_length=100)
    model = models.ForeignKey(Program, on_delete=models.PROTECT, related_name="program_altsubs")
    type_code = models.CharField(max_length=100)
    primary_material = models.ForeignKey(MaterialMaster, to_field="name", on_delete=models.PROTECT, related_name="primary_altsub_items")
    replacement_part = models.ForeignKey(MaterialMaster, to_field="name", on_delete=models.PROTECT, related_name="replacement_altsub_items")
    next_higher_assembly = models.CharField(max_length=100, blank=True, null=True)
    alternate_or_substitute_code = models.CharField(max_length=100)
    sub_code = models.CharField(max_length=100)
    wbs_element = models.CharField(max_length=100, blank=True, null=True)
    revision_level = models.CharField(max_length=100, blank=True, null=True)
    reason_for_change = models.CharField(max_length=100, blank=True, null=True)
    item_text_line = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateField(blank=True, null=True)
    upload = models.ForeignKey(AltSubUpload, null=True, on_delete=models.CASCADE, related_name="altsub_items")
