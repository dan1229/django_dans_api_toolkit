# base.pyi
from typing import Any, Dict, List, Optional
from rest_framework import serializers

# TYPE DEFINITIONS
class BaseSerializer(serializers.ModelSerializer):
    ref_fields: List[str]
    masked_fields: List[str]
    masked: bool
    ref_serializer: bool
    fields: Dict[str, serializers.Field]

    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
