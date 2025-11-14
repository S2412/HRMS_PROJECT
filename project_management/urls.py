from django.urls import path
from . import views

app_name = 'project'

urlpatterns = [
    path('', views.project_list_view, name='project_list'),
    path('add/', views.add_project_view, name='add_project'),
    path('edit/<int:pk>/', views.edit_project_view, name='edit_project'),
    path('assign/', views.assign_employee_view, name='assign_employee'),
    path('mappings/', views.mapping_list_view, name='mapping_list'),
]