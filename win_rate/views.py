import logging

from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.views import View
from djangoAPI.utils import check_access_key


from win_rate.service import handleGetWinRate

# Create your views here.
logger = logging.getLogger(__name__)


class GetWinRate(View):
    def post(self, request: HttpRequest) -> JsonResponse:
        try:
            if not check_access_key(request.headers.get("access-key")):
                return JsonResponse({'status': 'false', 'message': 'Unauthorized'}, status=401)
            return handleGetWinRate(request)
        except Exception as e:
            return JsonResponse({
                "ErrorMessage": str(e)
            })
