from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
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
]
