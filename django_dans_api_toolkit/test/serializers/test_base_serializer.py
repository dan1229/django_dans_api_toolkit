from django.test import TestCase
from .models import SampleModel, SampleSerializer


class BaseSerializerTestCase(TestCase):

    def setUp(self):
        self.instance = SampleModel(
            id=1, field1="value1", field2="value2", field3="value3"
        )

    def test_default_serialization(self):
        # note 'masked' is true by default
        serializer = SampleSerializer(self.instance)
        data = serializer.data
        self.assertIn("id", data)
        self.assertIn("field1", data)
        self.assertIn("field2", data)
        self.assertNotIn("field3", data)
        self.assertIn("field4", data)

    def test_not_masked_serialization(self):
        serializer = SampleSerializer(self.instance, masked=False)
        data = serializer.data
        self.assertIn("id", data)
        self.assertIn("field1", data)
        self.assertIn("field2", data)
        self.assertIn("field3", data)
        self.assertIn("field4", data)

    def test_masked_serialization(self):
        serializer = SampleSerializer(self.instance, masked=True)
        data = serializer.data
        self.assertIn("id", data)
        self.assertIn("field1", data)
        self.assertIn("field2", data)
        self.assertNotIn("field3", data)
        self.assertIn("field4", data)

    def test_not_ref_serialization(self):
        serializer = SampleSerializer(self.instance, ref_serializer=False)
        data = serializer.data
        self.assertIn("id", data)
        self.assertIn("field1", data)
        self.assertIn("field2", data)
        self.assertNotIn("field3", data)
        self.assertIn("field4", data)

    def test_ref_serialization(self):
        serializer = SampleSerializer(self.instance, ref_serializer=True)
        data = serializer.data
        self.assertIn("id", data)
        self.assertNotIn("field1", data)
        self.assertNotIn("field2", data)
        self.assertNotIn("field3", data)
        self.assertIn("field4", data)

    def test_custom_fields_serialization(self):
        serializer = SampleSerializer(self.instance, fields=["field1", "field3"])
        data = serializer.data
        self.assertIn("field1", data)
        self.assertIn("field3", data)
        self.assertNotIn("id", data)
        self.assertNotIn("field2", data)
        self.assertNotIn("field4", data)

    def test_combined_masked_and_ref_serialization(self):
        serializer = SampleSerializer(self.instance, masked=True, ref_serializer=True)
        data = serializer.data
        self.assertIn("id", data)
        self.assertNotIn("field1", data)
        self.assertNotIn("field2", data)
        self.assertNotIn("field3", data)
        self.assertIn("field4", data)
