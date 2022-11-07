import logging
import traceback

import ujson
from django.forms import model_to_dict

from mapping_source.models import GetPartMappingSourceOCRModel, GetPartMappingSourceModel
from mapping_source.serializers import GetPartMappingSourceModelSerializer, GetPartMappingSourceModelOCRSerializer

# Get an instance of a logger
logger = logging.getLogger(__name__)


def getPartMappingSourceSave(data: dict) -> GetPartMappingSourceModel:
    model = GetPartMappingSourceModelSerializer(data=data)
    if model.is_valid():
        try:
            model.save()
            logger.info("GetPartMappingSource request: {}".format(model.data))
            return GetPartMappingSourceModel.objects.filter(LineItemRecordID=model.data.get("LineItemRecordID"))[0]
        except Exception as e:
            logger.error(traceback.format_exc())
            logger.error(e)
    else:
        logger.error(traceback.format_exc())
        logger.error("GetPartMappingSourceModel error format")
        pass


def getPartMappingSourceOCRSave(data: dict) -> GetPartMappingSourceOCRModel:
    model = GetPartMappingSourceModelOCRSerializer(data=data)
    if model.is_valid():
        logger.info("GetPartMappingSourceOCR request: {}".format(model.validated_data))
        model.save()
        return GetPartMappingSourceOCRModel.objects.filter(id=model.data.get("id"))[0]
    else:
        logger.error("GetPartMappingSourceOCRModel error format")
        pass


def extractDataFromOCR(model: GetPartMappingSourceOCRModel) -> dict:
    return {
        "LineItemRecordID": model.LineItemRecordID,
        "base64string": model.File,
        "data_type": model.MimeType.lower()
    }


def updateGetPartMappingSourceOCRModel(data: dict, model: GetPartMappingSourceOCRModel):
    model.ProcessType = data.get("ProcessType")
    model.ocr_roi = ujson.dumps(data.get("RespData")[0].get("ocr_roi"),ensure_ascii=False)
    model.ocr_roi_cnt = data.get("RespData")[0].get("ocr_roi_cnt")
    model.save()
