import logging
import os

from django.http import HttpRequest, JsonResponse, HttpResponse
from django.views import View
from rest_framework.views import APIView

from djangoAPI.utils import check_access_key
from mapping_source.service import handleGetPartMappingSource, handleGetPartMappingSourceOCR

logger = logging.getLogger(__name__)


# Create your views here
class GetPartMappingSource(View):

    def post(self, request: HttpRequest) -> JsonResponse:
        try:
            if not check_access_key(request.headers.get("access-key")):
                return JsonResponse({'status': 'false', 'message': 'Unauthorized'}, status=401)
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
        if not check_access_key(request.headers.get("access-key")):
            return JsonResponse({'status':'false','message':'Unauthorized'}, status=401)
        return JsonResponse({"status": "alive"})
