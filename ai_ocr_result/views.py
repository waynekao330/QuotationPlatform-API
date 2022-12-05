from django.http import HttpRequest, JsonResponse
from rest_framework.views import APIView

from ai_ocr_result.service import handleGetAIOCRResult
from djangoAPI.utils import check_access_key


# Create your views here.
class GetAIOCRResult(APIView):

    def post(self, request: HttpRequest) -> JsonResponse:
        if not check_access_key(request.headers.get("access-key")):
            return JsonResponse({'status':'false','message':'Unauthorized'}, status=401)
        return handleGetAIOCRResult(request)
