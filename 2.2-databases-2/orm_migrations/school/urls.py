from django.contrib import admin
from django.urls import path, include
from school.views import students_list

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', students_list, name='students'),
]
