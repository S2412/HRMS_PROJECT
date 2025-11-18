from django.urls import path
from . import views

app_name = 'leave'  # ✅ This line registers the namespace

urlpatterns = [
    path('', views.leave_dashboard, name='leave_dashboard'),
    path('apply/', views.apply_leave, name='apply_leave'),
    path('admin/', views.admin_leave_list, name='admin_leave_list'),
    path('admin/approve/<int:leave_id>/', views.approve_leave, name='approve_leave'),
    path('admin/reject/<int:leave_id>/', views.reject_leave, name='reject_leave'),
    path('admin/approve/<int:leave_id>/', views.approve_leave, name='approve_leave'),
path('admin/reject/<int:leave_id>/', views.reject_leave, name='reject_leave'),

]