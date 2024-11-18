from django.urls import path
from . import views

urlpatterns = [
    path('add', views.DocumentViews.addDocument, name='add-document'),
    path('all-docs', views.DocumentViews.allDocuments, name='all-docs'),
    path('edit', views.DocumentViews.editDocument, name='edit-document'),
    path('edit/<str:file>', views.DocumentViews.editDocument, name='edit-document'),
    path('delete/<str:file>', views.DocumentViews.delDocument, name='delete-document'),
]
