# Generated by Django 4.1 on 2022-10-27 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GetPartMappingSourceModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('LineItemRecordID', models.TextField(blank=True, null=True)),
                ('TxNId', models.TextField(blank=True, null=True)),
                ('RFQRecordID', models.TextField(blank=True, null=True)),
                ('CustomerPartNumber', models.TextField(blank=True, null=True)),
                ('CustomerDescription', models.TextField(blank=True, null=True)),
                ('MOQ', models.IntegerField(blank=True, null=True)),
                ('EAU', models.IntegerField(blank=True, null=True)),
                ('PEComments', models.TextField(blank=True, null=True)),
                ('BoM', models.BooleanField(blank=True, null=True)),
                ('CrossReference', models.BooleanField(blank=True, null=True)),
                ('CutSheetWireList', models.BooleanField(blank=True, null=True)),
                ('Drawing', models.BooleanField(blank=True, null=True)),
                ('PRD', models.BooleanField(blank=True, null=True)),
                ('Sample', models.BooleanField(blank=True, null=True)),
                ('Currency_c', models.TextField(blank=True, null=True)),
                ('CreatedBy', models.TextField(blank=True, null=True)),
                ('IsParent', models.BooleanField(blank=True, null=True)),
                ('IsPost', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='GetPartMappingSourceOCRModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('TxNId', models.TextField(blank=True, null=True)),
                ('LineItemRecordID', models.TextField(blank=True)),
                ('FileName', models.TextField(blank=True)),
                ('MimeType', models.TextField(blank=True)),
                ('File', models.TextField(blank=True)),
                ('ProcessType', models.TextField(blank=True, null=True)),
                ('ocr_roi', models.TextField(blank=True, null=True)),
                ('ocr_roi_cnt', models.TextField(blank=True, null=True)),
                ('ai_mapping_result', models.BooleanField(default=False)),
                ('IsParent', models.BooleanField(blank=True, null=True)),
                ('IsPost', models.BooleanField(default=False)),
                ('RFQFormID', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
