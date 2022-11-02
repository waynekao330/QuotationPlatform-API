import json
import logging
from typing import Type

from ai_mapping_result.models import GetMappingSourceModel
from djangoAPI import settings
from djangoAPI.utils import patchAPI_with_bearer

# Get an instance of a logger
logger = logging.getLogger(__name__)
urlList = getattr(settings, "API_PATH", {})


def getPartMappingSourceSave(data: dict, line_item_record_id: str) -> Type[GetMappingSourceModel]:
    model = GetMappingSourceModel(
        LineItemRecordID=line_item_record_id,
        CustomerPartNumber=data.get("CustomerPartNumber"),
        Vendor=data.get("Vendor") if data.get("Vendor") else "",
        CustomerDescription=data.get("CustomerDescription"),
        QTY=data.get("QTY") if data.get("QTY") else "",
        Records=data.get("Records") if data.get("Records") else "",
        TxNId=data.get("TxNId")
    )
    logger.info("GetMappingSourceModelSerializer request: {}".format(model.__dict__))
    model.save()
    return model


def extractDataFromSource(model: GetMappingSourceModel) -> dict:
    return {
        "LineItemRecordID": model.LineItemRecordID,
        "prod_query_part_number": model.CustomerPartNumber,
        "prod_query": model.CustomerDescription,
        "QTY": model.QTY,
        "Vendor": model.Vendor
    }


def extractDataFromDict(model: dict) -> dict:
    return {
        "LineItemRecordID": model.get("LineitemRecordID"),
        "prod_query_part_number": model.get("prod_query_part_number"),
        "prod_query": model.get("prod_query"),
        "QTY": model.get("QTY"),
        "Vendor": model.get("Vendor")
    }


def updateGetMappingSourceModel(data: dict, model: GetMappingSourceModel) -> Type[GetMappingSourceModel]:
    logger.info(str(data))
    model.Records = str(data)
    model.save()
    return model


def sent_to_UpdateAIMappingResul(data: list):
    url = urlList.get("UpdateAIMappingResult")
    res = patchAPI_with_bearer(data, url)
    logger.info("SF_UpdateAIMappingResult res code: {}, content: {}".format(res.status_code, res.content))
