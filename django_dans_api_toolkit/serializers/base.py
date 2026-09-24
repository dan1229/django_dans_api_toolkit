from typing import Any, Dict, List, Optional
from rest_framework import serializers

"""
# ===================================================================================
# BASE SERIALIZER ===================================================================
# ===================================================================================
"""


class MaskedField(serializers.Field):  # type: ignore[type-arg]
    """
    Read-only placeholder for a masked field.

    Always renders as None, never reads the underlying attribute and never
    accepts input, so the key stays in the response without leaking its value.
    """

    def __init__(self, **kwargs: Any) -> None:
        kwargs["read_only"] = True
        super().__init__(**kwargs)

    def get_attribute(self, instance: Any) -> Any:
        return None

    def to_representation(self, value: Any) -> Any:
        # DRF short-circuits None attributes before calling this
        return None


class BaseSerializer(serializers.ModelSerializer):
    """
    BaseSerializer to inherit from

    :param bool masked:             If True, will mask the serializer.
                                    Based on `masked_fields` property. Fields in `masked_fields` will only
                                    show up if `masked` is False.
                                    NOTE: this is the default behavior.
    :param bool mask_as_null:       If True, masked fields keep their key with a None value
                                    instead of being removed. Default False (removed).
                                    Can also be set on the serializer class or its `Meta`.
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
    mask_as_null: bool = False
    ref_serializer: bool = False
    fields: Dict[str, serializers.Field]  # type: ignore[type-arg]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        # It's important to pop the kwargs before calling the superclass
        # since the superclass will throw an error if it receives an
        # unexpected keyword argument
        self.kwargs = kwargs
        self.masked = kwargs.pop("masked", self.masked)
        self.mask_as_null = kwargs.pop(
            "mask_as_null",
            getattr(getattr(self, "Meta", None), "mask_as_null", self.mask_as_null),
        )
        self.ref_serializer = kwargs.pop("ref_serializer", self.ref_serializer)

        # handle 'fields' keyword argument first since
        # it overrides the other logic
        fields: Optional[List[str]] = kwargs.pop("fields", None)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)
        else:
            # if masked serializer, null out (or remove) masked fields
            masked_fields = getattr(self.Meta, "masked_fields", self.masked_fields)
            if self.masked:
                for field in masked_fields:
                    if field not in self.fields:
                        continue
                    if self.mask_as_null:
                        self.fields[field] = MaskedField()
                    else:
                        self.fields.pop(field)

            # if ref serializer, remove ref fields
            ref_fields = getattr(self.Meta, "ref_fields", self.ref_fields)
            if self.ref_serializer:
                for field in ref_fields:
                    self.fields.pop(field, None)

        # Instantiate the superclass normally
        # NOTE: the placement of this is important
        # since we want to remove fields before
        # the superclass is instantiated
        super().__init__(*args, **kwargs)
