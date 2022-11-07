import base64
import time
import traceback
from random import choice

from django.http import JsonResponse, HttpRequest

from ai_mapping_result.utils import sent_to_UpdateAIMappingResul
from djangoAPI import settings
from djangoAPI.utils import getJsonFromRequest, postAPI, get_api_without_wait
from .utils import *

urlList = getattr(settings, "API_PATH", {})
logger = logging.getLogger(__name__)


def handleGetPartMappingSource(request: HttpRequest) -> JsonResponse:
    # 1-1 儲存完資料後檢查是否有CustomerPartNumber & Description 有得話呼叫AI mapping
    try:
        data = getJsonFromRequest(request)
        logger.info("handleGetPartMappingSource request body: {}".format(data))
        res = getattr(settings, "MOCK_MAPPING_RESPONSE", {})
        res_data = []
        RFQFormID = ""
        for i in data.get("Data"):
            i["TxNId"] = data.get("TxNId")
            i["IsParent"] = True
            model = getPartMappingSourceSave(i)
            # 檢查是否CustomerPartNumber & Description 有值
            if model:
                res_data.append(model_to_dict(model))
                RFQFormID = model.RFQRecordID

        #res["data"] = res_data
        # 都做完才做ai mapping 跟發送SF
        sent_ai_mapping(data.get("TxNId"), RFQFormID)
        return JsonResponse(res)
    except Exception as e:
        logger.error(traceback.format_exc())
        logger.error(e)
        return JsonResponse({
            "ErrorMessage": str(e)
        })


def handleGetPartMappingSourceOCR(request: HttpRequest) -> JsonResponse:
    data = getJsonFromRequest(request)
    response = {
        'ErrorMessage': ' ',
        'ProcessType': 'S',
    }
    res_data = []
    for i in data.get("FilesList"):
        try:
            model = getPartMappingSourceOCRSave(i)
            if model:
                data = extractDataFromOCR(model)
                res = postAPI(data, urlList.get("QP_GetPartNoMappingSource_OCR"))
                updateGetPartMappingSourceOCRModel(res.get("response"), model)
                aa = res.get("response").get("RespData")[0]
                print(aa)
                if aa:
                    res_data.append(aa)
        except Exception as e:
            print(e)
            pass
    response['RespData'] = res_data
    return JsonResponse(response)


def sent_ai_mapping(TxNId: str, RFQFormID: str):
    # 這裡做兩件事情，從1-1取值，再從1-2取列表，通通集合起來做ai mapping 在呼叫後端
    # 這裡先建一個表以CustomerDescription 為key 為了好merge
    sf_ob = {}
    post_data = []
    part_mapping_list = GetPartMappingSourceModel.objects.filter(TxNId=TxNId).filter(
        IsPost=False)
    ocr_list = GetPartMappingSourceOCRModel.objects.filter(RFQFormID=RFQFormID).filter(
        IsPost=False)
    # 這邊要去組request
    ai_mapping_request = {
        "dict_data": {
            "TxNId": TxNId,
            "Data": [
                {
                    "RFQFormID": RFQFormID
                }
            ]
        }}
    # 這邊先看1-1有沒有CustomerPartNumber&Description 有的話先加入patch_data
    for model in part_mapping_list:
        model.IsPost = True
        model.save()
        if model.CustomerDescription:
            # 建立mapping 物件
            sf_key = base64.b64encode(model.CustomerDescription.encode('UTF-8')).decode('UTF-8')
            sf_ob[sf_key] = {
                "RFQFormID":model.RFQRecordID,
                "LineItemRecordID": model.LineItemRecordID,
                "IsParent": model.IsParent,
                "CustomerPartNo": model.CustomerPartNumber,
                "CustomerDescription": model.CustomerDescription,
                "PEComments":model.PEComments,
                "Vendor": None,
                "qty": None
            }
            post_data.append({
                "LineItemRecordID": model.LineItemRecordID,
                "CustomerPartNumber": model.CustomerPartNumber,
                "Description": model.CustomerDescription,
            })
    # 1-2 取值
    time.sleep(10)
    for ocr in ocr_list:
        ocr.IsPost = True
        ocr.save()
        cor_json = ujson.loads(ocr.ocr_roi)
        for roi in cor_json[0]:
            # 建立mapping 物件
            sf_key = base64.b64encode(roi.get("CustomerDescription").encode('UTF-8')).decode('UTF-8')
            sf_ob[sf_key] = {
                "RFQFormID":ocr.RFQFormID,
                "LineItemRecordID": ocr.LineItemRecordID,
                "IsParent": ocr.IsParent,
                "CustomerPartNo": roi.get("CustomerPartNumber"),
                "Vendor": roi.get("Vendor"),
                "qty": roi.get("QTY"),
                "CustomerDescription": roi.get("CustomerDescription")
            }
            post_data.append({
                "LineItemRecordID": ocr.LineItemRecordID,
                "CustomerPartNumber": roi.get("CustomerPartNumber"),
                "Description": roi.get("CustomerDescription"),
            })

    # 處理完所有檔案發送到ai mapping
    logger.info("sf_ob: {}".format(ujson.dumps(sf_ob,ensure_ascii=False)))
    ai_mapping_request["dict_data"]["Data"][0]["Records"] = post_data
    logger.info("ai_mapping_request: {}".format(ujson.dumps(ai_mapping_request,ensure_ascii=False)))
    ai_mapping_res = postAPI(ai_mapping_request, urlList.get("GetAIMappingResult"))
    logger.info("ai_mapping_res: {}".format(ujson.dumps(ai_mapping_res,ensure_ascii=False)))
    logger.info("GetAIMappingResult all done to ai mapping")
    if ai_mapping_res:
        # 發送有結果，進行處理
        for res_data in ai_mapping_res.get("response").get("RespData"):
            # 這邊要去找之前建立的sf object 填進去
            sf_key = base64.b64encode(res_data.get("CustomerDescription").encode('UTF-8')).decode('UTF-8')
            if sf_ob.get(sf_key):
                sf_ob[sf_key][
                    "Records"] = res_data.get("Records")
    # 都填完了就準備新增到SF
    sf_req = {
        "ProcessType": "S",
        "ErrorMessage": "",
        "RespData": list(sf_ob.values())
    }
    patch_data = [{"PartMappingJSON": ujson.dumps(sf_req,ensure_ascii=False),
                   "RFQFormID": RFQFormID
                   }]
    logger.info("sent_to_UpdateAIMappingResul: {}".format(ujson.dumps(patch_data)))
    sent_to_UpdateAIMappingResul(patch_data)
    logger.info("GetAIMappingResult all done update to SF_UpdateAIMappingResult")
