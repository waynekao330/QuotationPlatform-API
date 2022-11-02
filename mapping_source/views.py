import logging

from django.http import HttpRequest, JsonResponse
from django.views import View
from rest_framework.views import APIView

from mapping_source.service import handleGetPartMappingSource, handleGetPartMappingSourceOCR

logger = logging.getLogger(__name__)


# Create your views here
class GetPartMappingSource(View):

    def post(self, request: HttpRequest) -> JsonResponse:
        try:
            return handleGetPartMappingSource(request)
        except Exception as e:
            return JsonResponse({
                "ErrorMessage": str(e)
            })


class GetPartMappingSourceOCR(View):
    def post(self, request: HttpRequest) -> JsonResponse:
        try:
            return handleGetPartMappingSourceOCR(request)
        except Exception as e:
            return JsonResponse({
                "ErrorMessage": str(e)
            })


class CheckAlive(APIView):

    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse({"status": "alive"})
