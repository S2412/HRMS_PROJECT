from django.urls import path
from . import views

app_name = 'leave'

urlpatterns = [
    path('apply/', views.apply_leave, name='apply_leave'),
    path('history/', views.view_leave_history, name='view_leave_history'),
    path('cancel/<int:leave_id>/', views.cancel_leave, name='cancel_leave'),
    path('admin/list/', views.admin_leave_list, name='admin_leave_list'),
    path('admin/approve/<int:leave_id>/', views.approve_leave, name='approve_leave'),
]