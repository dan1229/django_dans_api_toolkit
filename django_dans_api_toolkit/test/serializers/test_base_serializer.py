from django.test import TestCase
from .models import SampleModel, SampleSerializer


class BaseSerializerTestCase(TestCase):

    def setUp(self):
        self.instance = SampleModel(
            id=1, field1="value1", field2="value2", field3="value3"
        )

    def test_default_serialization(self):
        serializer = SampleSerializer(self.instance)
        data = serializer.data
        self.assertEqual(set(data.keys()), {"id", "field1", "field2", "field3"})

    def test_masked_serialization(self):
        serializer = SampleSerializer(self.instance, masked=True)
        data = serializer.data
        self.assertEqual(set(data.keys()), {"id", "field1", "field2"})

    def test_ref_serialization(self):
        serializer = SampleSerializer(self.instance, ref_serializer=True)
        data = serializer.data
        self.assertEqual(set(data.keys()), {"id", "field1", "field2"})

    def test_custom_fields_serialization(self):
        serializer = SampleSerializer(self.instance, fields=["field1", "field3"])
        data = serializer.data
        self.assertEqual(set(data.keys()), {"field1", "field3"})

    def test_combined_masked_and_ref_serialization(self):
        serializer = SampleSerializer(self.instance, masked=True, ref_serializer=True)
        data = serializer.data
        self.assertEqual(set(data.keys()), {"id", "field1", "field2"})
