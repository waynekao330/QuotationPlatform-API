from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.views import View

from ai_mapping_result.service import handleGetAIMappingResult


# Create your views here.
class GetAIMappingResult(View):
    def get(self, request: HttpRequest, lineItemRecordID: str) -> JsonResponse:
        try:
            return handleGetAIMappingResult(lineItemRecordID)
        except Exception as e:
            return JsonResponse({
                "ErrorMessage": str(e)
            })
