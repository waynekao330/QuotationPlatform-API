from django.db import models


# Create your models here.
class GetWinRate(models.Model):
    TxNId = models.TextField(blank=True, null=True, unique=False)
    RFQFormID = models.TextField(blank=True, null=True, unique=False)
    LineItemRecordID = models.TextField(blank=True, null=True, unique=False)
    amount = models.TextField(blank=True, null=True, unique=False)
    rawMaterialCost = models.TextField(blank=True, null=True, unique=False)
    laborTime = models.TextField(blank=True, null=True, unique=False)
    laborCost = models.TextField(blank=True, null=True, unique=False)
    directMFGCosts = models.TextField(blank=True, null=True, unique=False)
    toolingCost = models.TextField(blank=True, null=True, unique=False)
    packingMatCost = models.TextField(blank=True, null=True, unique=False)
    totalMatYieldLoss = models.TextField(blank=True, null=True, unique=False)
    SMTFee = models.TextField(blank=True, null=True, unique=False)
    winRate = models.TextField(blank=True, null=True, unique=False)
