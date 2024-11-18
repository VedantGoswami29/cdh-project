from django.urls import path
from  . import views

urlpatterns = [
    path('add', views.StudentViews.addStudent),
    path('get', views.StudentViews.getStudent),
    path('edit', views.StudentViews.editStudent),
    path('bulk-edit', views.StudentViews.bulkEditStudents),
    path('delete', views.StudentViews.delStudent),
    path('delete/<str:roll_number>', views.StudentViews.delStudent),
]
