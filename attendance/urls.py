from django.urls import path
from . import views

app_name = 'attendance'  # ✅ This registers the namespace

urlpatterns = [
    path('mark/', views.mark_attendance, name='mark_attendance'),
    path('manual/', views.mark_attendance_form, name='mark_attendance_form'),
    path('view/', views.view_attendance, name='view_attendance'),
    path('regularize/', views.submit_regularization_request, name='regularize'),
    path('monthly/', views.monthly_attendance, name='monthly_attendance'),
    path('summary/', views.attendance_summary, name='attendance_summary'),
    path('export/', views.export_attendance_csv, name='export_attendance_csv'),
]