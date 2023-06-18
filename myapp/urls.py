# from django.urls import path
# from myapp import views
# from .views import LeaveRequestView

# urlpatterns = [
#     path('api/', views.api_list),
#     path('apidetails/<int:pk>/', views.api_detail),
#     path('api/leave-request/', LeaveRequestView.as_view(), name='leave-request'),
# ]

from django.urls import path
from .views import (
    EmployeeListCreateView,
    EmployeeRetrieveUpdateDeleteView,
    LeaveRequestCreateView,
    EmployeeLeaveRequestView,
    SearchView,
    VacationAttachmentUploadView,
    EmployeeLeaveRemainingView
)

urlpatterns = [
    path('api/employees/', EmployeeListCreateView.as_view(), name='employee-list-create'),
    path('api/employees/<int:pk>/', EmployeeRetrieveUpdateDeleteView.as_view(), name='employee-retrieve-update-delete'),
    path('api/leave-request/', LeaveRequestCreateView.as_view(), name='leave-request-create'),
    path('api/employee-leave-request/<int:employee_id>/', EmployeeLeaveRequestView.as_view(), name='employee-leave-request'),
    path('api/employee-leave-request/<int:employee_id>/<str:status>/', EmployeeLeaveRequestView.as_view(), name='employee-leave-request-status'),
    path('api/search/?query=', SearchView.as_view(), name='search'),
    path('api/vacation-upload/', VacationAttachmentUploadView.as_view(), name='vacation-upload'),
    path('api/employee-leave-remaining/', EmployeeLeaveRemainingView.as_view(), name='employee_leave_remaining'),

]
