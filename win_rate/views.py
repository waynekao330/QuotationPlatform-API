import logging

from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.views import View

from win_rate.service import handleGetWinRate

# Create your views here.
logger = logging.getLogger(__name__)


class GetWinRate(View):
    def post(self, request: HttpRequest) -> JsonResponse:
        try:
            return handleGetWinRate(request)
        except Exception as e:
            return JsonResponse({
                "ErrorMessage": str(e)
            })
