from django.contrib import admin

from mapping_source.models import GetPartMappingSourceModel, GetPartMappingSourceOCRModel

# Register your models here.
admin.site.register(GetPartMappingSourceModel)
admin.site.register(GetPartMappingSourceOCRModel)
