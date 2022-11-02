import logging

from django.http import HttpRequest, JsonResponse

from djangoAPI import settings
from djangoAPI.utils import getJsonFromRequest, postAPI
from win_rate.utils import getWinRateSave, extractDataFromWinRate, updateWinRateModel

urlList = getattr(settings, "API_PATH", {})
logger = logging.getLogger(__name__)


def handleGetWinRate(request: HttpRequest) -> JsonResponse:
    try:
        logger.info("handleGetWinRate request body: {}".format(request.body))
        data = getJsonFromRequest(request)
        model = getWinRateSave(data)
        response = {
            'ErrorMessage': "",
            'ProcessType': "S",
            "RFQFormID": model.RFQFormID,
            "LineItemRecordID": model.LineItemRecordID
        }
        data = extractDataFromWinRate(model)
        res = postAPI(data, urlList.get("WinRate"))
        logger.info("[updateGetPartMappingSourceOCRModel] [res]: {}".format(res))
        updateWinRateModel(res, model)
        response["winRate"] = model.winRate
        return JsonResponse(response)

    except Exception as e:
        return JsonResponse({
            "ErrorMessage": str(e)
        })
