from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'director'
urlpatterns = [
    path('', views.index, name='index'),
    path('stream/', views.streamDetectionView, name='stream'),
    path("stream/<str:camera_ip>/", views.videoDetect, name="videoDetect"),
    path('addCamera/', views.addCameraView, name='addCamera'),
    path('cameraDetail/<pk>', views.cameraDetailView, name='cameraDetail'),
    path("<str:camera_ip>/", views.videoStream, name="videoStream"),
]
