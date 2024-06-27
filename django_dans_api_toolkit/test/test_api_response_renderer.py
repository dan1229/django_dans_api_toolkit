from django.test import TestCase, RequestFactory
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from ..api_response_renderer import ApiResponseRenderer
from ..api_response_handler import ApiResponseHandler


class MockView(APIView):
    renderer_classes = [ApiResponseRenderer]

    def get(self, request, *args, **kwargs):
        return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        return Response({"results": {"key": "value"}})


class ApiResponseRendererTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.view = MockView.as_view()

    def test_render_with_detail(self):
        request = self.factory.get("/mock-view/")
        response = self.view(request)

        renderer = ApiResponseRenderer()
        rendered_content = renderer.render(
            response.data, renderer_context={"response": response}
        )

        self.assertIn(b'"message": "Not found"', rendered_content)
        self.assertIn(b'"results": null', rendered_content)
        self.assertIn(b'"error_fields": null', rendered_content)

    def test_render_without_message(self):
        request = self.factory.post("/mock-view/")
        response = self.view(request)

        renderer = ApiResponseRenderer()
        rendered_content = renderer.render(
            response.data, renderer_context={"response": response}
        )

        self.assertIn(b'"message": "Successfully completed request."', rendered_content)
        self.assertIn(b'"results": {"key": "value"}', rendered_content)
        self.assertIn(b'"error_fields": null', rendered_content)

    def test_render_without_results(self):
        request = self.factory.get("/mock-view/")
        response = Response({"message": "Custom message"}, status=status.HTTP_200_OK)

        renderer = ApiResponseRenderer()
        rendered_content = renderer.render(
            response.data, renderer_context={"response": response}
        )

        self.assertIn(b'"message": "Custom message"', rendered_content)
        self.assertIn(b'"results": null', rendered_content)
        self.assertIn(b'"error_fields": null', rendered_content)

    def test_render_without_error_fields(self):
        request = self.factory.get("/mock-view/")
        response = Response(
            {"message": "Another custom message", "results": {"key": "value"}},
            status=status.HTTP_200_OK,
        )

        renderer = ApiResponseRenderer()
        rendered_content = renderer.render(
            response.data, renderer_context={"response": response}
        )

        self.assertIn(b'"message": "Another custom message"', rendered_content)
        self.assertIn(b'"results": {"key": "value"}', rendered_content)
        self.assertIn(b'"error_fields": null', rendered_content)

    def test_render_combined_scenario(self):
        request = self.factory.get("/mock-view/")
        response = Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        renderer = ApiResponseRenderer()
        rendered_content = renderer.render(
            response.data, renderer_context={"response": response}
        )

        self.assertIn(b'"message": "Error. Please try again later."', rendered_content)
        self.assertIn(b'"results": null', rendered_content)
        self.assertIn(b'"error_fields": null', rendered_content)
