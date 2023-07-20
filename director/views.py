from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import StreamingHttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators import gzip
from .forms import CameraForm
from .models import CameraModel
from .multiCameraDetect import generate
from .multiCameraStream import gen


# Create your views here.
@login_required
@gzip.gzip_page
def index(request):
    cameras = CameraModel.objects.filter(user_id=request.user.pk)
    context = {"cameras": cameras,
               }
    return render(request=request, template_name="director/index.html", context=context)


@login_required
def streamDetectionView(request):
    cameras = CameraModel.objects.all()
    camera_list = []
    i = 0
    for camera in cameras:
        if "rtsp:" in camera.web_address:
            camera_list.append(camera)
            i += 1
            if i == 2:
                break
    context = {"cameras": camera_list,
               }
    return render(request=request, template_name="director/stream.html", context=context)


@login_required
def addCameraView(request):
    context = {}
    form = CameraForm(request.POST or None)
    if form.is_valid():
        c_form = form.save(commit=False)
        c_form.user_id = request.user
        c_form.save()
        return redirect('director:index')

    context['form'] = form
    return render(request, "director/add_camera.html", context)



@login_required
def cameraDetailView(request, pk):
    key = settings.GOOGLE_API_KEY

    camera = get_object_or_404(CameraModel, pk=pk)
    form = CameraForm(request.POST or None, instance=camera)
    if request.user.is_active:
        if request.method == 'POST':
            if 'camera_update_btn' in request.POST:
                if form.is_valid():
                    form.save()
            elif 'camera_delete_btn' in request.POST:
                camera.delete()
                return redirect('director:index')
            return redirect('director:cameraDetail', pk=camera.pk)
    context = {
        'camera': camera,
        'form': form,
        'key': key,
    }
    return render(request, 'director/camera_detail.html', context)


@login_required
def videoStream(request, camera_ip):
    return StreamingHttpResponse(gen(camera_ip), content_type='multipart/x-mixed-replace; boundary=frame')


@login_required
def videoDetect(request, camera_ip):
    return StreamingHttpResponse(generate(camera_ip), content_type='multipart/x-mixed-replace; boundary=frame')
