from django.contrib import admin
from .models import EmployeeInfo, LeaveRequest

# Register your models here.
admin.site.register(EmployeeInfo)
admin.site.register(LeaveRequest)