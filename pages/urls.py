from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    # Dil sayfaları için URL patterns
    path('courses/<str:language>/', views.show_language_page, name='language_page'),
    path('courses/<str:language>/<str:slug>/', views.get_language_detail, name='language_detail'),
]