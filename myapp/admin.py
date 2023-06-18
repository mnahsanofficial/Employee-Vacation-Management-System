# from django.contrib import admin
# from .models import Employee
# # Register your models here.

# admin.site.register(Employee)

from django.contrib import admin
from .models import Employee, LeaveRequest

class LeaveRequestInline(admin.StackedInline):
    model = LeaveRequest
    extra = 0

class EmployeeAdmin(admin.ModelAdmin):
    inlines = [LeaveRequestInline]

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(LeaveRequest)
