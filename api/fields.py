from django.contrib.gis.geos import Point
from rest_framework.fields import CharField


class LocationField(CharField):
    def to_representation(self, value):
        return [value.x, value.y]

    def to_internal_value(self, data):
        data = data.lstrip('(').rstrip(')')
        x, y = [float(col) for col in data.split(',')]
        return Point(x=x, y=y)
