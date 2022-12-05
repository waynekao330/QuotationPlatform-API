import logging
import os
import traceback

import ujson
from django.forms import model_to_dict
from django.http import JsonResponse

from ai_mapping_result.models import GetMappingSourceModel
from ai_mapping_result.utils import getPartMappingSourceSave, extractDataFromSource, updateGetMappingSourceModel, \
    sent_to_UpdateAIMappingResul, extractDataFromDict
from djangoAPI import settings
from djangoAPI.utils import postAPI
from mapping_source.models import GetPartMappingSourceOCRModel, GetPartMappingSourceModel

urlList = getattr(settings, "API_PATH", {})
logger = logging.getLogger(__name__)


def handleGetAIMappingResult(lineItemRecordID: str) -> JsonResponse:
    logger.info("lineItemRecordID request body: {}".format(lineItemRecordID))
    response = {
        'ErrorMessage': ' ',
        'ProcessType': 'S',
    }
    res_data = []
    patch_data = []
    # jwt_token = get_jwt_token()
    data = GetPartMappingSourceOCRModel.objects.filter(ai_mapping_result=False) \
        .filter(LineItemRecordID=lineItemRecordID)
    for i in data:
        # change record to ai_mapping_result to avoid dup call
        i.ai_mapping_result = True
        i.save()

        try:
            i_json = ujson.loads(i.ocr_roi)
            for roi in i_json:
                model = getPartMappingSourceSave(roi, lineItemRecordID)
                if model:
                    data = extractDataFromSource(model)
                    res = postAPI(data, os.getenv("GetAIMappingResult"))
                    model = updateGetMappingSourceModel(res.get("response").get("RespData")[0], model)
                    patch_data.append({
                        "PartMappingJSON": ujson.dumps(res.get("response")),
                        "RFQFormID": lineItemRecordID
                    })
                    res_data.append(model_to_dict(model))
        except Exception as e:
            logger.error(e)
            pass
    logger.info("GetAIMappingResult all done update to SF_UpdateAIMappingResult")
    sent_to_UpdateAIMappingResul(patch_data)
    response['RespData'] = res_data
    return JsonResponse(response)


# 這邊是由1-1觸發呼叫ai mapping
def sent_ai_mapping(model: GetPartMappingSourceModel):
    try:
        # 再檢查一次
        if model.CustomerPartNumber and model.Description:
            req = getPartMappingSourceSave({
                "CustomerPartNumber": model.CustomerPartNumber,
                "CustomerDescription": model.Description,
                "TxNId": model.TxNId
            }, model.LineItemRecordID)
            if req:
                data = extractDataFromSource(req)
                res = postAPI(data, os.getenv("GetAIMappingResult"))
                # 把isParent塞進RespData
                if res.get("RespData"):
                    for resp in res.get("RespData"):
                        resp["IsParent"] = model.IsParent
                req = updateGetMappingSourceModel(res, req)
                logger.info("1-1 call ai mapping: {}".format(model_to_dict(req)))
    except Exception as e:
        logger.error(str(e))


def ocr_call_ai_mapping(resp_list: list, LineitemRecordID: str, TxNId: str, IsParent: bool):
    try:
        for resp in resp_list:
            for ori in resp.get("ocr_roi"):
                req = {
                    "LineItemRecordID": resp.get("LineItemRecordID"),
                    "prod_query_part_number": ori.get("CustomerPartNumber"),
                    "prod_query": ori.get("CustomerDescription"),
                    "QTY": ori.get("QTY"),
                    "Vendor": ori.get("Vendor")
                }
                print("req for ai mapping".format(req))
                if req:
                    res = postAPI(req, os.getenv("GetAIMappingResult"))
                    print("ocr aimapping res: {}".format(res))
                    if res:
                        # ai mapping res RespData add IsParent
                        for r in res.get("response").get("RespData"):
                            r["IsParent"] = IsParent
                        # create ai mapping
                        req = getPartMappingSourceSave({
                            "CustomerPartNumber": ori.get("CustomerPartNumber"),
                            "CustomerDescription": ori.get("CustomerDescription"),
                            "QTY": ori.get("QTY"),
                            "Vendor": ori.get("Vendor"),
                            "Records": ujson.dumps(res),
                            "TxNId": TxNId
                        }, LineitemRecordID)
                    logger.info("1-2 call ai mapping: {}".format(req))
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        print(traceback.format_exc())
