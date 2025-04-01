from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('courses/<str:language>/', views.show_language_page, name='language_page'),
    path('courses/<str:language>/<str:slug>/', views.get_language_detail, name='language_detail'),
    path('courses/<str:category>/<str:slug>/delete/', views.delete_page, name='delete_page'),
    path('search/', views.search, name='search'),
    path('page/edit/<int:page_id>/', views.edit_page, name='edit_page'),
    path('page/save/<int:page_id>/', views.save_page, name='save_page'),
    path('api/pages/<int:page_id>/delete/', views.delete_page, name='delete_page'),
]