from django.test import TestCase
from ...serializers.base import MaskedField
from .models import SampleModel, SampleSerializer


class BaseSerializerTestCase(TestCase):

    def setUp(self) -> None:
        self.instance = SampleModel(
            id=1, field1="value1", field2="value2", field3="value3", field4="value4"
        )

    def test_default_serialization(self) -> None:
        # note 'masked' is true by default
        serializer = SampleSerializer(self.instance)
        data = serializer.data
        self.assertIn("id", data)
        self.assertIn("field1", data)
        self.assertIn("field2", data)
        self.assertNotIn("field3", data)
        self.assertIn("field4", data)

    def test_not_masked_serialization(self) -> None:
        serializer = SampleSerializer(self.instance, masked=False)
        data = serializer.data
        self.assertIn("id", data)
        self.assertIn("field1", data)
        self.assertIn("field2", data)
        self.assertIn("field3", data)
        self.assertIn("field4", data)

    def test_masked_serialization(self) -> None:
        serializer = SampleSerializer(self.instance, masked=True)
        data = serializer.data
        self.assertIn("id", data)
        self.assertIn("field1", data)
        self.assertIn("field2", data)
        self.assertNotIn("field3", data)
        self.assertIn("field4", data)

    def test_not_ref_serialization(self) -> None:
        serializer = SampleSerializer(self.instance, ref_serializer=False)
        data = serializer.data
        self.assertIn("id", data)
        self.assertIn("field1", data)
        self.assertIn("field2", data)
        self.assertNotIn("field3", data)
        self.assertIn("field4", data)

    def test_ref_serialization(self) -> None:
        serializer = SampleSerializer(self.instance, ref_serializer=True)
        data = serializer.data
        self.assertIn("id", data)
        self.assertNotIn("field1", data)
        self.assertNotIn("field2", data)
        self.assertNotIn("field3", data)
        self.assertIn("field4", data)

    def test_custom_fields_serialization(self) -> None:
        serializer = SampleSerializer(self.instance, fields=["field1", "field3"])
        data = serializer.data
        self.assertIn("field1", data)
        self.assertIn("field3", data)
        self.assertNotIn("id", data)
        self.assertNotIn("field2", data)
        self.assertNotIn("field4", data)

    def test_combined_masked_and_ref_serialization(self) -> None:
        serializer = SampleSerializer(self.instance, masked=True, ref_serializer=True)
        data = serializer.data
        self.assertIn("id", data)
        self.assertNotIn("field1", data)
        self.assertNotIn("field2", data)
        self.assertNotIn("field3", data)
        self.assertIn("field4", data)

    def test_fields_override_masked_and_ref(self) -> None:
        serializer = SampleSerializer(
            self.instance, fields=["field3"], masked=True, ref_serializer=True
        )
        data = serializer.data
        self.assertIn("field3", data)
        self.assertNotIn("id", data)
        self.assertNotIn("field1", data)
        self.assertNotIn("field2", data)
        self.assertNotIn("field4", data)

    def test_empty_fields(self) -> None:
        serializer = SampleSerializer(self.instance, fields=[])
        data = serializer.data
        self.assertNotIn("id", data)
        self.assertNotIn("field1", data)
        self.assertNotIn("field2", data)
        self.assertNotIn("field3", data)
        self.assertNotIn("field4", data)

    def test_invalid_field_in_fields(self) -> None:
        serializer = SampleSerializer(self.instance, fields=["invalid_field"])
        data = serializer.data
        self.assertNotIn("id", data)
        self.assertNotIn("field1", data)
        self.assertNotIn("field2", data)
        self.assertNotIn("field3", data)
        self.assertNotIn("field4", data)

    def test_all_fields_explicitly(self) -> None:
        serializer = SampleSerializer(
            self.instance, fields=["id", "field1", "field2", "field3", "field4"]
        )
        data = serializer.data
        self.assertIn("id", data)
        self.assertIn("field1", data)
        self.assertIn("field2", data)
        self.assertIn("field3", data)
        self.assertIn("field4", data)

    def test_masked_and_custom_fields(self) -> None:
        serializer = SampleSerializer(self.instance, fields=["field3"], masked=True)
        data = serializer.data
        self.assertIn("field3", data)
        self.assertNotIn("id", data)
        self.assertNotIn("field1", data)
        self.assertNotIn("field2", data)
        self.assertNotIn("field4", data)

    def test_ref_and_custom_fields(self) -> None:
        serializer = SampleSerializer(
            self.instance, fields=["field3"], ref_serializer=True
        )
        data = serializer.data
        self.assertIn("field3", data)
        self.assertNotIn("id", data)
        self.assertNotIn("field1", data)
        self.assertNotIn("field2", data)
        self.assertNotIn("field4", data)


class MaskAsNullTestCase(TestCase):
    """`mask_as_null` is opt-in; the default keeps removing masked fields."""

    def setUp(self) -> None:
        self.instance = SampleModel(
            id=1, field1="value1", field2="value2", field3="value3", field4="value4"
        )

    def test_default_still_removes_masked_key(self) -> None:
        self.assertNotIn("field3", SampleSerializer(self.instance).data)

    def test_opt_in_kwarg_keeps_key_as_none(self) -> None:
        data = SampleSerializer(self.instance, mask_as_null=True).data
        self.assertIn("field3", data)
        self.assertIsNone(data["field3"])
        self.assertNotIn("value3", data.values())
        self.assertEqual(data["field4"], "value4")

    def test_opt_in_via_meta(self) -> None:
        class NullingSerializer(SampleSerializer):
            class Meta(SampleSerializer.Meta):
                mask_as_null = True

        self.assertIsNone(NullingSerializer(self.instance).data["field3"])

    def test_opt_in_not_masked_shows_value(self) -> None:
        data = SampleSerializer(self.instance, masked=False, mask_as_null=True).data
        self.assertEqual(data["field3"], "value3")

    def test_opt_in_ignores_input_for_masked_field(self) -> None:
        serializer = SampleSerializer(
            data={"field1": "a", "field2": "b", "field3": "secret", "field4": "d"},
            mask_as_null=True,
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertNotIn("field3", serializer.validated_data)

    def test_opt_in_skips_masked_names_that_are_not_fields(self) -> None:
        class GhostSerializer(SampleSerializer):
            class Meta(SampleSerializer.Meta):
                masked_fields = ["not_a_field", "field3"]

        data = GhostSerializer(self.instance, mask_as_null=True).data
        self.assertNotIn("not_a_field", data)
        self.assertIsNone(data["field3"])

    def test_default_skips_masked_names_that_are_not_fields(self) -> None:
        class GhostSerializer(SampleSerializer):
            class Meta(SampleSerializer.Meta):
                masked_fields = ["not_a_field", "field3"]

        self.assertNotIn("field3", GhostSerializer(self.instance).data)

    def test_masked_field_to_representation_is_none(self) -> None:
        field = MaskedField()
        self.assertTrue(field.read_only)
        self.assertIsNone(field.to_representation("anything"))

    def test_mask_as_null_kwarg_not_forwarded(self) -> None:
        serializer = SampleSerializer(self.instance, mask_as_null=True)
        self.assertNotIn("mask_as_null", serializer.kwargs)
