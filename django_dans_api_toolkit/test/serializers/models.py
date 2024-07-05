from django.db import models

from ...serializers.base import BaseSerializer


class SampleModel(models.Model):
    field1 = models.CharField(max_length=100)  # type: ignore[var-annotated]
    field2 = models.CharField(max_length=100)  # type: ignore[var-annotated]
    field3 = models.CharField(max_length=100)  # type: ignore[var-annotated]
    field4 = models.CharField(max_length=100)  # type: ignore[var-annotated]


class SampleSerializer(BaseSerializer):
    class Meta:
        model = SampleModel
        fields = "__all__"
        ref_fields = ["field1", "field2"]
        masked_fields = ["field3"]
