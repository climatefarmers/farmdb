from rest_framework import serializers
from .models import Person, Farm, PersonToRoleToOrg, SurveyAnswers
from .utils.survey.parser import parse_survey

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'email', 'phone',
                  'address', 'comm_pref']

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonToRoleToOrg
        fields = ['person', 'role', 'organization']

class FarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farm
        fields = ['name', 'description', 'website', 'address',
                  'farm_size_approx', 'date_joined', 'public_profile',
                  'survey_answers']

class SurveyAnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyAnswers
        fields = ['farm_type', 'production_methods', 'main_products',
                  'soil', 'tillage', 'fertilization', 'irrigation',
                  'uses_icides', 'receives_funding']


class FarmerSurveySerializer(serializers.ModelSerializer):
    person = PersonSerializer()
    role = RoleSerializer()
    farm = FarmSerializer()
    survey_answers = SurveyAnswersSerializer()

    def create(self, validated_data: dict):
        parsed = parse_survey(validated_data)
        pass