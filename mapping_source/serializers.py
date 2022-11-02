from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from ai_mapping_result.models import GetMappingSourceModel
from mapping_source.models import GetPartMappingSourceModel, GetPartMappingSourceOCRModel
from win_rate.models import GetWinRate


class GetPartMappingSourceModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GetPartMappingSourceModel
        fields = "__all__"


class GetPartMappingSourceModelOCRSerializer(serializers.ModelSerializer):
    class Meta:
        model = GetPartMappingSourceOCRModel
        fields = "__all__"


class GetGetMappingSourceModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GetMappingSourceModel
        fields = "__all__"


class GetWinRateModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GetWinRate
        fields = "__all__"


def validate_password(self, value: str) -> str:
    """
    Hash value passed by user.

    :param value: password of a user
    :return: a hashed version of the password
    """
    return make_password(value)
