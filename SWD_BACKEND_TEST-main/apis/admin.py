from django.contrib import admin
from apis.models import *

# Register your models here.

@admin.register(Personnel)
class PersonnelAdmin(admin.ModelAdmin):
    list_display = ('id','first_name','last_name','school_class','personnel_type')
    # readonly_fields = ["create_date"]

@admin.register(StudentSubjectsScore)
class StudentSubjectsScoreAdmin(admin.ModelAdmin):
    list_display = ('id','student','subjects','credit','score')

@admin.register(Subjects)
class SubjectsAdmin(admin.ModelAdmin):
    list_display = ('id','title')

@admin.register(SchoolStructure)
class SchoolStructureAdmin(admin.ModelAdmin):
    list_display = ('id','title','parent')
