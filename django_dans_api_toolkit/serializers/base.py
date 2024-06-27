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
                                    show up if `masked` is False.
                                    NOTE: this is the default behavior.
    :param bool ref_serializer:     If True, will return a reference serializer.
                                    Based on `ref_fields` property. Fields in `ref_fields` will only show
                                    up if `ref_serializer` is False. If `ref_fields` is not provided,
                                    all fields will be returned.
    :param List[str] fields:        Additional kwargs 'field' that controls which fields to include.
                                    NOTE: This overrides both `masked` and `ref_serializer` logic.
    """

    ref_fields: List[str] = []
    masked_fields: List[str] = []
    masked: bool = True
    ref_serializer: bool = False

    def __init__(self, *args: Any, **kwargs: Any) -> None:

        # handle 'fields' keyword argument first since
        # it overrides the other logic
        fields: Optional[List[str]] = kwargs.pop("fields", None)

        # handle masked serializer
        masked = kwargs.pop("masked", self.masked)
        masked_fields = getattr(self.Meta, "masked_fields", self.masked_fields)

        # handle ref serializer
        ref_serializer = kwargs.pop("ref_serializer", self.ref_serializer)
        ref_fields = getattr(self.Meta, "ref_fields", self.ref_fields)

        # If fields is explicitly passed, it overrides masked and ref_serializer logic
        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)
        else:
            # if masked serializer, remove masked fields
            if masked:
                for field in masked_fields:
                    self.fields.pop(field, None)

            # if ref serializer, remove ref fields
            if ref_serializer:
                for field in ref_fields:
                    self.fields.pop(field, None)

        # Instantiate the superclass normally
        # NOTE: the placement of this (after the ref/masked logic)
        # is VERY important
        super().__init__(*args, **kwargs)
