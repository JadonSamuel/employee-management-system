from django.urls import path
from .import views


urlpatterns = [
    path('', views.index, name='index'),
    path('model/',views.model,name='model'),
    path('add_employee/',views.add_employee, name= 'add_employee'),
    path('edit_employee/<int:employee_id>/',views.edit_employee, name ='edit_employee'),
    path('delete_employee/<int:employee_id>/',views.delete_employee,name='delete_employee'),
    path('custom_login/',views.custom_login, name='custom_login'),
    path('register/',views.register,name ='register'),
    path('logout/',views.logout, name='logout')

]




