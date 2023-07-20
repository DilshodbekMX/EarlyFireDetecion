import cv2
from .models import CameraModel


def find_camera(ids):
    cameras_list = CameraModel.objects.get(id=ids)
    cameras = [cameras_list.web_address]
    return cameras[int(0)]

def gen(camera):
    cam = find_camera(camera)
    came = IPWebCam(cam)
    while True:
        frame = came.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

class IPWebCam(object):
    def __init__(self, camera_ip):
        self.url = cv2.VideoCapture(camera_ip)

    def __del__(self):
        cv2.destroyAllWindows()

    def get_frame(self):
        success, imgNp = self.url.read()
        resize = cv2.resize(imgNp, (640, 640), interpolation=cv2.INTER_LINEAR)
        ret, jpeg = cv2.imencode('.jpg', imgNp)
        return jpeg.tobytes()
