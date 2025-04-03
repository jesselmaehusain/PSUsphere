from django.contrib import admin # type: ignore
from .models import College, Program, Organization, Student, OrgMember

admin.site.register(College)
admin.site.register(Program)
admin.site.register(Organization)
admin.site.register(Student)
admin.site.register(OrgMember)
