#!/bin/bash
QP_GetPartNoMappingSource_OCR="http://162.133.78.212:5000/from-b64?key=mykey"
GetAIMappingResult="http://162.133.78.212:5000/mapping_prod?key=mykey"
JWTLogin="https://api.bizlinktech.com:8082/mule-api/basic/token"
UpdateAIMappingResult="http://api.bizlinktech.com:8079/mule-api/salesforce/SF_UpdateAIMappingResult/UAT"
UpdateAIMapping="http://127.0.0.1:8000/GetAIMappingResult/"
WinRate="http://162.133.78.212:6000/winrate/predict"