from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.serializers import *
from .models import *

class CategoryTreeSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = SchoolStructure
        fields = ('id', 'title', 'parent')


class CreateStudentSubjectsScoreSerializer(serializers.Serializer):
    first_name = CharField(allow_null=True,allow_blank=True)
    last_name = CharField(allow_null=True,allow_blank=True)
    subject_title = CharField(allow_null=True,allow_blank=True)
    score = IntegerField(allow_null=False)
    


