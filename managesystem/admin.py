from django.contrib import admin
from .models import Work, Employee, WorkUnit, Term, Result, Attachment

# Register your models here
admin.site.register(Work)
admin.site.register(Employee)
admin.site.register(WorkUnit)
admin.site.register(Term)
admin.site.register(Result)
admin.site.register(Attachment)
