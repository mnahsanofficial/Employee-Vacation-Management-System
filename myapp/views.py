from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Employee, LeaveRequest
from .serializers import EmployeeSerializer, LeaveRequestSerializer
from myapp import serializers
from rest_framework import status
from rest_framework.parsers import FileUploadParser
from django.db.models import Count

class EmployeeListCreateView(APIView):
    def get(self, request):
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class EmployeeRetrieveUpdateDeleteView(APIView):
    def get_object(self, pk):
        try:
            return Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            raise serializers.ValidationError("Employee not found.")

    def get(self, request, pk):
        employee = self.get_object(pk)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

    def put(self, request, pk):
        employee = self.get_object(pk)
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        employee = self.get_object(pk)
        employee.delete()
        return Response(status=204)

class LeaveRequestCreateView(APIView):
    def get(self, request, format=None):
        leave_requests = LeaveRequest.objects.all()
        serializer = LeaveRequestSerializer(leave_requests, many=True)
        return Response(serializer.data)

    def post(self, request):
        employee_id = request.data.get('employee')

        vacation_count = LeaveRequest.objects.filter(employee_id=employee_id).count()
        if vacation_count >= 4:
            return Response({'detail': 'Maximum number of vacations reached for this employee.'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = LeaveRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_object(self, pk):
        try:
            return LeaveRequest.objects.get(pk=pk)
        except LeaveRequest.DoesNotExist:
            raise Response(status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, format=None):
        leave_request_id = request.data.get('id')
        try:
            leave_request = LeaveRequest.objects.get(pk=leave_request_id)
        except LeaveRequest.DoesNotExist:
            return Response({'detail': 'Leave request not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = LeaveRequestSerializer(leave_request, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk, format=None):
        leave_request_id = request.data.get('id')
        leave_request_id.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def patch(self, request, pk, format=None):
        leave_request_id = request.data.get('id')
        leave_request_id.status = 'Approved'
        leave_request_id.save()
        return Response(status=status.HTTP_200_OK)
    

class EmployeeLeaveRequestView(APIView):
    def get(self, request, employee_id, status=None, format=None):
        employee = Employee.objects.get(id=employee_id)
        leave_requests = LeaveRequest.objects.filter(employee=employee)

        if status is not None:
            leave_requests = leave_requests.filter(status=status)

        serializer = LeaveRequestSerializer(leave_requests, many=True)
        return Response(serializer.data)
    

class SearchView(APIView):
    def get(self, request, format=None):
        search_query = request.query_params.get('query', '')

        employees = Employee.objects.filter(name__icontains=search_query)
        employee_serializer = EmployeeSerializer(employees, many=True)

        leave_requests = LeaveRequest.objects.filter(employee__name__icontains=search_query)
        leave_request_serializer = LeaveRequestSerializer(leave_requests, many=True)

        response_data = {
            'employees': employee_serializer.data,
            'leave_requests': leave_request_serializer.data
        }

        return Response(response_data)
    

class VacationAttachmentUploadView(APIView):
    parser_class = (FileUploadParser,)

    def get(self, request, format=None):
        leave_requests = LeaveRequest.objects.all()
        serializer = LeaveRequestSerializer(leave_requests, many=True)
        return Response(serializer.data)

class EmployeeLeaveRemainingView(APIView):
    def get(self, request, format=None):
        employees = Employee.objects.annotate(
            leaves_taken=Count('leaverequest')
        ).values('id', 'name','leaves_taken')

        for employee in employees:
            employee['leaves_remaining'] = 4 - employee['leaves_taken']
            del employee['leaves_taken']

        return Response(employees, status=200)