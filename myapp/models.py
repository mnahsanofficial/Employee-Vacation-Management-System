from django.db import models
import uuid
from django import forms

# Create your models here.

class Employee(models.Model):
    employeeid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, blank=True,)
    name = models.CharField(max_length=50, blank=True, default='')
    email = models.EmailField(max_length=50, blank=True,unique=True, default='')
    title = models.CharField(max_length=50, blank=True, default='')
    description = models.CharField(max_length=150, blank=True, default='')
    hiringdate = models.DateField(max_length=40, blank=True, default='')

    def __str__(self) :
        return self.name

class LeaveRequest(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE,to_field='employeeid')
    start_date = models.DateField(max_length=45, blank=True, default='')
    end_date = models.DateField(max_length=45, blank=True, default='')
    attachment_url = models.FileField(upload_to='attachments/', blank=True, null=True)
    status = models.CharField(max_length=25,choices=(('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')))

    def __str__(self):
        return f"Leave request for {self.employee} - {self.start_date} to {self.end_date}"
