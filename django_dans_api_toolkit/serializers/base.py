from typing import Any, List
from rest_framework import serializers

"""
# ===================================================================================
# BASE SERIALIZER ===================================================================
# ===================================================================================
"""


class BaseSerializer(serializers.ModelSerializer):  # type: ignore[type-arg]
    """
    BaseSerializer to inherit from

    :param bool masked:             If True, will mask the serializer.
                                    Based on `masked_fields` property. Fields in `masked_fields` will only
                                    show up if `masked` is False
    :param bool ref_serializer:     If True, will return a reference serializer.
                                    Based on `ref_fields` property, fields in `ref_fields` will only show
                                    up if `ref_serializer` is False. If `ref_fields` is not provided,
                                    all fields will be returned.
    :param str[] fields:            Additional kwargs 'field' that controls which fields to include
    """

    ref_fields: List[str] = []
    masked_fields: List[str] = []
    masked = True
    ref_serializer = False

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        # save kwargs for later
        self.kwargs = kwargs

        # handle 'fields' keyword argument
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop("fields", None)

        # if masked serializer, remove masked fields
        self.masked = kwargs.pop("masked", self.masked)
        masked_fields = getattr(self.Meta, "masked_fields", [])
        if self.masked:
            for field in masked_fields:
                self.fields.pop(field)

        # if ref serializer, remove ref fields
        self.ref_serializer = kwargs.pop("ref_serializer", self.ref_serializer)
        ref_fields = getattr(self.Meta, "ref_fields", [])
        if self.ref_serializer:
            for field in ref_fields:
                self.fields.pop(field)

        # Instantiate the superclass normally
        super(BaseSerializer, self).__init__(*args, **kwargs)

        # Drop any fields that are not specified in the `fields` argument.
        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
