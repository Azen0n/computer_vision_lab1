from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('log/', views.processing, name='log'),
    path('backward_log/', views.processing, name='backward_log'),
    path('power_law/', views.processing, name='power_law'),
    path('binary/', views.processing, name='binary'),
    path('bit_plane_slicing/', views.processing, name='bit_plane_slicing'),
    path('square_filter/', views.processing, name='square_filter'),
    path('median_filter/', views.processing, name='median_filter'),
]
