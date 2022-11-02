from django.db import models


# Create your models here.
class GetMappingSourceModel(models.Model):
    id = models.AutoField(primary_key=True)
    TxNId = models.TextField(blank=True, null=True, unique=False)
    LineItemRecordID = models.TextField(blank=True, null=False)
    CustomerPartNumber = models.TextField(blank=True, null=False)
    Vendor = models.TextField(blank=True, null=False)
    CustomerDescription = models.TextField(blank=True, null=False)
    Records = models.TextField(blank=True, null=False)
    QTY = models.TextField(blank=True, null=False)
    isPost = models.BooleanField(default=False)
