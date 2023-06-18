# from rest_framework import serializers
# from myapp.models import Contact
# from myapp.models import LeaveRequest


# class ContactSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Contact
#         fields = ['employeeid','name','email', 'title', 'description','hiringdate']


# class LeaveRequestSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = LeaveRequest
#         fields = '__all__'

from rest_framework import serializers
from .models import Employee, LeaveRequest

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class LeaveRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = '__all__'
