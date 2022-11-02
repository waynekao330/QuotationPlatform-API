from django.http import HttpRequest, JsonResponse
from rest_framework.views import APIView

from ai_ocr_result.service import handleGetAIOCRResult


# Create your views here.
class GetAIOCRResult(APIView):

    def post(self, request: HttpRequest) -> JsonResponse:
        return handleGetAIOCRResult(request)
