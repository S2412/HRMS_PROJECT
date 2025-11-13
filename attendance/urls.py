from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    path('mark/', views.mark_attendance, name='mark_attendance'),
    path('mark/form/', views.mark_attendance_form, name='mark_attendance_form'),
    path('view/', views.view_attendance, name='view_attendance'),
    path('summary/', views.monthly_summary, name='monthly_summary'),
    path('regularize/<int:attendance_id>/', views.request_regularization, name='request_regularization'),
    path('hr/approvals/', views.hr_approval_list, name='hr_approval_list'),
    path('approve/<int:request_id>/', views.approve_request, name='approve_request'),
    path('reject/<int:request_id>/', views.reject_request, name='reject_request'),
    path('export/', views.export_attendance_csv, name='export_attendance_csv'),
    path('dashboard/', views.dashboard, name='dashboard'),
     path('regularize/<int:attendance_id>/', views.send_regularization_request, name='send_regularization_request'),

]