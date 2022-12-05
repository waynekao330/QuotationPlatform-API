from django.contrib import admin

from mapping_source.models import GetPartMappingSourceModel, GetPartMappingSourceOCRModel, AiMappingResult

# Register your models here.
admin.site.register(GetPartMappingSourceModel)
admin.site.register(GetPartMappingSourceOCRModel)
admin.site.register(AiMappingResult)
