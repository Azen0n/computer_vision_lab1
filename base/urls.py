from django.urls import path
from . import views

urlpatterns = [
    path('', views.lab3, name='index'),
    path('lab1', views.lab1, name='lab1'),
    path('lab2', views.lab2, name='lab2'),
    path('lab3', views.lab3, name='lab3'),
    path('log/', views.processing, name='log'),
    path('backward_log/', views.processing, name='backward_log'),
    path('power_law/', views.processing, name='power_law'),
    path('binary/', views.processing, name='binary'),
    path('bit_plane_slicing/', views.processing, name='bit_plane_slicing'),
    path('cutting_out_intensity_range/', views.processing, name='cutting_out_intensity_range'),
    path('square_filter/', views.processing, name='square_filter'),
    path('median_filter/', views.processing, name='median_filter'),
    path('gaussian_filter/', views.processing, name='gaussian_filter'),
    path('sigma_filter/', views.processing, name='sigma_filter'),
    path('unsharp_masking/', views.processing, name='unsharp_masking'),
    path('metric/', views.metric, name='metric'),
    path('noise/', views.processing, name='noise'),
    path('sobel/', views.processing, name='sobel'),
    path('laplacian_of_gaussian/', views.processing, name='laplacian_of_gaussian'),
    path('difference_of_gaussian/', views.processing, name='difference_of_gaussian'),
]
