from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class PositionChoices(models.IntegerChoices):
        GSC_LEAD = 1, "Global Supply Chain Lead"
        GSC_PLANNER = 2, "Global Supply Chain Planning Specialist"

    position = models.IntegerField(choices=PositionChoices.choices, verbose_name="position", default=2)
