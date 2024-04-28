from typing import Any, Dict, List, Optional
from rest_framework import serializers

"""
# ===================================================================================
# BASE SERIALIZER ===================================================================
# ===================================================================================
"""


class BaseSerializer(serializers.ModelSerializer):
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
    masked: bool = True
    ref_serializer: bool = False
    fields: Dict[str, serializers.Field]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.kwargs = kwargs  # Save kwargs for later

        # handle 'fields' keyword argument
        fields: Optional[List[str]] = kwargs.pop("fields", None)

        # if masked serializer, remove masked fields
        self.masked = kwargs.pop("masked", self.masked)
        masked_fields = getattr(self.Meta, "masked_fields", self.masked_fields)
        if self.masked:
            for field in masked_fields:
                self.fields.pop(field, None)

        # if ref serializer, remove ref fields
        self.ref_serializer = kwargs.pop("ref_serializer", self.ref_serializer)
        ref_fields = getattr(self.Meta, "ref_fields", self.ref_fields)
        if self.ref_serializer:
            for field in ref_fields:
                self.fields.pop(field, None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        # Drop any fields that are not specified in the `fields` argument
        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)
