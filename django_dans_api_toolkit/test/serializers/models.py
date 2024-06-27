from django.db import models
from rest_framework import serializers

from ...serializers.base import BaseSerializer


class SampleModel(models.Model):
    field1 = models.CharField(max_length=100)
    field2 = models.CharField(max_length=100)
    field3 = models.CharField(max_length=100)


class SampleSerializer(BaseSerializer):
    class Meta:
        model = SampleModel
        fields = "__all__"
        ref_fields = ["field1", "field2"]
        masked_fields = ["field3"]
