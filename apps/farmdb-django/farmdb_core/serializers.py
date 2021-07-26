from rest_framework import serializers
from rest_framework_gis.serializers import GeoModelSerializer
from address.models import Country, State, Locality, Address
from .models import (Organization, Field, Role, Person, Farm, PersonToRoleToOrg,
                     SurveyAnswers, CommunicationPreferences)
from .utils.survey.parser import parse_survey


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['name']
        extra_kwargs = {
            'name': {'validators':[]} # We're maintaining uniqueness through get_or_create further down
        }


class StateSerializer(serializers.ModelSerializer):
    country = CountrySerializer()

    class Meta:
        model = State
        fields = ['name', 'country']


class LocalitySerializer(serializers.ModelSerializer):
    state = StateSerializer()

    class Meta:
        model = Locality
        fields = ['name', 'state']


class AddressSerializer(serializers.ModelSerializer):
    locality = LocalitySerializer()

    class Meta:
        model = Address
        fields = ['street_number', 'route', 'raw', 'locality']


class CommunicationPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunicationPreferences
        fields = ['comm_channel']


class SurveyAnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyAnswers
        fields = ['farm_type', 'production_methods', 'main_products',
                  'soil', 'tillage', 'fertilization', 'irrigation',
                  'uses_icides', 'receives_funding']


class PersonSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    comm_pref = CommunicationPreferencesSerializer()

    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'email', 'phone',
                  'address', 'comm_pref']


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['role']


class FieldSerializer(GeoModelSerializer):
    farm = serializers.ReadOnlyField(source='farm.name')
    class Meta:
        model = Field
        fields = ['id', 'field_name', 'geom', 'farm']

class FarmSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    survey_answers = SurveyAnswersSerializer()
    fields = FieldSerializer(many=True, read_only=True)
    class Meta:
        model = Farm
        fields = ['id', 'name', 'website', 'address',
                  'farm_size_approx', 'survey_answers', 'fields']


class PersonToRoleToOrgSerializer(serializers.ModelSerializer):
    person = PersonSerializer()
    role = RoleSerializer()
    organization = FarmSerializer()

    class Meta:
        model = PersonToRoleToOrg
        fields = ['person', 'role', 'organization']


    def create(self, validated_data: dict):

        address = validated_data['person'].pop('address')
        validated_data['organization'].pop('address')
        comm_pref = validated_data['person'].pop('comm_pref')
        survey_answers = validated_data['organization'].pop('survey_answers')

        country, _ = Country.objects.get_or_create(
            name=address['locality']['state']['country']['name'],
            code=''
        )
        state, _ = State.objects.get_or_create(
            name=address['locality']['state']['name'],
            code='',
            country=country
        )
        locality, _ = Locality.objects.get_or_create(
            name=address['locality']['name'],
            postal_code='',
            state=state
        )
        address, _ = Address.objects.get_or_create(
            street_number=address['street_number'],
            route=address['route'],
            raw=address['raw'],
            locality=locality
        )

        comm_pref, _ = CommunicationPreferences.objects.get_or_create(
            comm_channel=comm_pref['comm_channel'])
        
        person, _ = Person.objects.get_or_create(
            **validated_data['person'], 
            address=address,
            comm_pref=comm_pref
        )


        survey_answers, _ = SurveyAnswers.objects.get_or_create(**survey_answers)

        farm, _ = Farm.objects.get_or_create(
            **validated_data['organization'],
            address=address,
            survey_answers=survey_answers
        )

        role, _ = Role.objects.get_or_create(**validated_data['role'])  # 1 for Farmer

        person_to_role_to_org, created = PersonToRoleToOrg.objects.get_or_create(
            person=person,
            role=role,
            organization=farm
        )

        if created:
            return person_to_role_to_org
        person_to_role_to_org.organization = farm
        return person_to_role_to_org
