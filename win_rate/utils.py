import logging

from mapping_source.serializers import GetWinRateModelSerializer
from win_rate.models import GetWinRate

logger = logging.getLogger(__name__)


def getWinRateSave(data: dict) -> GetWinRate:
    model = GetWinRateModelSerializer(data=data)
    if model.is_valid():
        logger.info("GetWinRate request: {}".format(model.validated_data))
        model.save()
        return GetWinRate.objects.filter(id=model.data.get("id"))[0]
    else:
        logger.error("model invalid")
        pass


def extractDataFromWinRate(data: GetWinRate) -> [dict]:
    return [{
        "Amount": float(data.amount),
        "Raw Material Cost": float(data.rawMaterialCost),
        "Labor Cost": float(data.laborCost),
        "Labor Time": float(data.laborTime),
        "Direct MFG Costs": float(data.directMFGCosts)
    }]


def updateWinRateModel(data: dict, model: GetWinRate):
    model.winRate = data.get("Win-rate")[0]
    model.save()
