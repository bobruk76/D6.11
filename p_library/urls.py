from django.contrib import admin
from django.urls import path
from .views import *


app_name = 'p_library'
urlpatterns = [
    path('author/create', AuthorCreate.as_view(), name='author_create'),
    path('author/', AuthorList.as_view(), name='author_list'),
    path('author/<int:pk>/', AuthorUpdate.as_view(), name='author_edit'),
    path('author/<int:pk>/delete/', AuthorDelete.as_view(), name='author_delete'),

    path('author/create_many', author_create_many, name='author_create_many'),
    path('author_book/create_many', books_authors_create_many, name='author_book_create_many'),

    path('reader/create', ReaderCreate.as_view(), name='reader_create'),
    path('reader/', ReaderList.as_view(), name='reader_list'),
    path('reader/<int:pk>/', ReaderUpdate.as_view(), name='reader_update'),
    path('reader/<int:pk>/delete/', ReaderDelete.as_view(), name='reader_delete'),
]