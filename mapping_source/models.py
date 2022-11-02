from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models


# Create your models here.
class GetPartMappingSourceModel(models.Model):
    id = models.AutoField(primary_key=True)
    LineItemRecordID = models.TextField(blank=True, null=True, unique=False)
    TxNId = models.TextField(blank=True, null=True, unique=False)
    RFQRecordID = models.TextField(blank=True, null=True, unique=False)
    CustomerPartNumber = models.TextField(blank=True, null=True)
    CustomerDescription = models.TextField(blank=True, null=True)
    MOQ = models.IntegerField(blank=True, null=True)
    EAU = models.IntegerField(blank=True, null=True)
    PEComments = models.TextField(blank=True, null=True)
    BoM = models.BooleanField(blank=True, null=True)
    CrossReference = models.BooleanField(blank=True, null=True)
    CutSheetWireList = models.BooleanField(blank=True, null=True)
    Drawing = models.BooleanField(blank=True, null=True)
    PRD = models.BooleanField(blank=True, null=True)
    Sample = models.BooleanField(blank=True, null=True)
    Currency_c = models.TextField(blank=True, null=True)
    CreatedBy = models.TextField(blank=True, null=True)
    IsParent = models.BooleanField(blank=True, null=True)
    IsPost = models.BooleanField(default=False)


class GetPartMappingSourceOCRModel(models.Model):
    id = models.AutoField(primary_key=True)
    TxNId = models.TextField(blank=True, null=True, unique=False)
    LineItemRecordID = models.TextField(blank=True, null=False)
    FileName = models.TextField(blank=True, null=False)
    MimeType = models.TextField(blank=True, null=False)
    File = models.TextField(blank=True, null=False)
    ProcessType = models.TextField(blank=True, null=True)
    ocr_roi = models.TextField(blank=True, null=True)
    ocr_roi_cnt = models.TextField(blank=True, null=True)
    ai_mapping_result = models.BooleanField(default=False)
    IsParent = models.BooleanField(blank=True, null=True)
    IsPost = models.BooleanField(default=False)
    RFQFormID = models.TextField(blank=True, null=True)

