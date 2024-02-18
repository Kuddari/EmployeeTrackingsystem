from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *

from .admin_resources import UserResource

class UserAdmin(ImportExportModelAdmin):
    resource_class = UserResource

admin.site.unregister(User)
admin.site.register(User, UserAdmin)



@admin.register(Employee)
class EmployeeAdmin(ImportExportModelAdmin):
    def employee_name(self, obj):
        return f"{obj.username.first_name} {obj.username.last_name}"
    employee_name.short_description = 'Name'  # Sets the column name

    list_display = ('employee_name', 'position', 'branch', 'profile')
    search_fields = ('username__first_name', 'username__last_name', 'position', 'branch')

@admin.register(Work)
class WorkAdmin(ImportExportModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

@admin.register(Setunit)
class SetunitAdmin(ImportExportModelAdmin):
    list_display = ('name', 'position', 'minunit', 'maxunit')
    search_fields = ('name__name', 'position')

@admin.register(Result)
class ResultAdmin(ImportExportModelAdmin):
    list_display = ('employee', 'work', 'term1', 'term2', 'total', 'employee_score', 'dean_score', 'result_score', 'file')
    search_fields = ('employee__username__first_name', 'employee__username__last_name', 'work__name__name')

@admin.register(Save)
class SaveAdmin(ImportExportModelAdmin):
    list_display = ('employee_id', 'employee_firstname', 'employee_lastname', 'work', 'description', 'total', 'employee_score', 'dean_score', 'result_score', 'file', 'date')
    search_fields = ('employee_firstname', 'employee_lastname', 'work')


@admin.register(Evaluation)
class EvaluationAdmin(ImportExportModelAdmin):
    list_display = ('employee', 'evaluation_score', 'date')
    search_fields = ('employee__username__first_name', 'employee__username__last_name', 'evaluation_score')


