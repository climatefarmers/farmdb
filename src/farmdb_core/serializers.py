from rest_framework import serializers
from .models import Person, Farm, PersonToRoleToOrg, SurveyAnswers


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonToRoleToOrg

class FarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farm

class SurveyAnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyAnswers


class FarmerSurveySerializer(serializers.ModelSerializer):
    person = PersonSerializer()
    role = RoleSerializer()
    farm = FarmSerializer()
    survey_answers = SurveyAnswersSerializer()

    def create(self, validated_data: dict):
        pass