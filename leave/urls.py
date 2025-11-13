from django.urls import path
from . import views

app_name = 'leave'

urlpatterns = [
<<<<<<< HEAD
    path('', views.leave_list, name='leave_list'),
    path('apply/', views.leave_apply, name='leave_apply'),
    path('<int:pk>/', views.leave_detail, name='leave_detail'),

    
=======
    path('apply/', views.apply_leave, name='apply_leave'),
    path('history/', views.view_leave_history, name='view_leave_history'),
    path('cancel/<int:leave_id>/', views.cancel_leave, name='cancel_leave'),
    path('admin/list/', views.admin_leave_list, name='admin_leave_list'),
    path('admin/approve/<int:leave_id>/', views.approve_leave, name='approve_leave'),
>>>>>>> c9590ad3056f752fdb52e31082e9d3d99b03e3af
]