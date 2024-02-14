from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *

from .admin_resources import UserResource

class UserAdmin(ImportExportModelAdmin):
    resource_class = UserResource

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Employee, ImportExportModelAdmin)
admin.site.register(Work, ImportExportModelAdmin)
admin.site.register(Setunit, ImportExportModelAdmin)
admin.site.register(Result, ImportExportModelAdmin)
admin.site.register(Save, ImportExportModelAdmin)
admin.site.register(Evaluation, ImportExportModelAdmin)

