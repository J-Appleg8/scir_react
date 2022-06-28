from functools import cached_property
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Color(models.Model):
    name = models.CharField(max_length=20)
    is_primary = models.BooleanField(default=False)
    red = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(255)])
    green = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(255)])
    blue = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(255)])

    @cached_property
    def hex_code(self):

        def color_hex_pair(color_value:int) -> str:
            return hex(color_value)[2:].rjust(2, '0')

        r = color_hex_pair(self.red)
        g = color_hex_pair(self.green)
        b = color_hex_pair(self.blue)

        return f'#{r}{g}{b}'

    __str__ = __repr__ = lambda self: self.name

class Shape(models.Model):
    name = models.CharField(max_length=20)

    __str__ = __repr__ = lambda self: self.name
