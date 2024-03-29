import logging
import os
import traceback

from django.http import HttpRequest, JsonResponse

from ai_mapping_result.models import GetMappingSourceModel
from ai_mapping_result.service import ocr_call_ai_mapping
from ai_mapping_result.utils import sent_to_UpdateAIMappingResul
from djangoAPI import settings
from djangoAPI.utils import getJsonFromRequest, postAPI
from mapping_source.models import GetPartMappingSourceModel, GetPartMappingSourceOCRModel
from mapping_source.utils import getPartMappingSourceOCRSave, extractDataFromOCR, updateGetPartMappingSourceOCRModel

urlList = getattr(settings, "API_PATH", {})
logger = logging.getLogger(__name__)


def handleGetAIOCRResult(request: HttpRequest) -> JsonResponse:
    # 1-2 紀錄同一個line item id的檔案數，最後一筆時發送到後端API
    try:
        logger.info("handleGetAIOCRResult request body: {}".format(request.body))
        data = getJsonFromRequest(request)
        response = {
            'ErrorMessage': '',
            'ProcessType': 'S',
        }
        res_data = []
        TxNId = data.get("TxNId")
        RFQFormID = data.get("RFQFormID")
        ocr_error_chain = []
        if data.get("Data"):
            for i in data.get("Data"):
                try:
                    lineItemRecordID = i.get("LineItemRecordID")
                    if i.get("Attachments"):
                        # 這裡紀錄檔案數量，當到的時候發送到後端
                        count = 0
                        for attach in i.get("Attachments"):
                            attach["LineItemRecordID"] = lineItemRecordID
                            attach["TxNId"] = TxNId
                            attach["IsParent"] = False
                            attach["RFQFormID"] = RFQFormID
                            model = getPartMappingSourceOCRSave(attach)
                            if model and getattr(model,"File"):
                                # 呼叫OCR
                                data = extractDataFromOCR(model)
                                
                                # data["base64string"] = str(base64.b64encode(str(data["base64string"]).encode()))
                                res = postAPI(data, os.getenv("QP_GetPartNoMappingSource_OCR"))
                                logger.info("1-2Respdata: {}".format(res))
                                if res:
                                    updateGetPartMappingSourceOCRModel(res, model)
                                    logger.info("[updateGetPartMappingSourceOCRModel] [res]: {}".format(res))
                                    resp_data = res.get("RespData")
                                    print("resp_data: {}".format(resp_data))
                                    if resp_data:
                                        res_data.append(resp_data)
                                    else:
                                        res_data = {"error": "OCR API error"}
                                        ocr_error_chain.append(attach.get("FileName"))
                                else:
                                    ocr_error_chain.append(attach.get("FileName"))
                except Exception as e:
                    logger.error(traceback.format_exc())
                    pass
            try:
                if res:    
                    response["ProcessType"] = "S"
                    #response['RespData'] = res_data
            except Exception as e:
                    logger.error(traceback.format_exc())
                    pass
        response["ErrorMessage_OCR"] = ocr_error_chain
        logger.info("response:{}".format(response))
        return JsonResponse(response)
        
    except Exception as e:
        logger.error(traceback.format_exc())
        return JsonResponse({
            "ErrorMessage": str(e)
        })
