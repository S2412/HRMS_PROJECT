from django.urls import path
from . import views

urlpatterns = [
    path('', views.leave_list, name='leave_list'),
    path('apply/', views.leave_apply, name='leave_apply'),
    path('<int:pk>/', views.leave_detail, name='leave_detail'),

    
]