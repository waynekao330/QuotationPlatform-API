"""djangoAPI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import to include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

import ai_mapping_result.views
import ai_ocr_result.views
import mapping_source.views
import win_rate.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('GetPartMappingSource', mapping_source.views.GetPartMappingSource.as_view()),
    # path('GetPartMappingSourceOCR', mapping_source.views.GetPartMappingSourceOCR.as_view()),
    path('GetPartMappingSourceOCR', ai_ocr_result.views.GetAIOCRResult.as_view()),
    path('GetWinRate', win_rate.views.GetWinRate.as_view()),
    path('GetAIMappingResult/<lineItemRecordID>', ai_mapping_result.views.GetAIMappingResult.as_view()),
    path('CheckAlive', mapping_source.views.CheckAlive.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
