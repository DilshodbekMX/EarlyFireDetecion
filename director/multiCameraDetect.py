import math
import time

import cv2
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from ultralytics import YOLO

from .models import CameraModel

cred = credentials.Certificate('./googleServices/firedetection.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()


def find_camera(ids):
    cameras_list = CameraModel.objects.get(id=ids)
    cameras = [cameras_list.web_address]
    return cameras[int(0)]


def generate(pk):
    cam = find_camera(pk)
    yolo_output = video_detection(cam, pk)
    for detection_ in yolo_output:
        ref, buffer = cv2.imencode('.jpg', detection_)

        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def video_detection(path_x, pk):
    camera_pk = CameraModel.objects.get(pk=pk)
    print(camera_pk.web_address)
    alert_camera = db.collection("AlertCamera").document(str(camera_pk.pk) + camera_pk.camera_name)

    video_capture = path_x
    detected_camera = CameraModel.objects.filter(web_address=video_capture)[0]
    # Create a Webcam Object
    cap = cv2.VideoCapture(video_capture)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    # out=cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc('M', 'J', 'P','G'), 10, (frame_width, frame_height))

    model = YOLO("YOLO-Weights/best.pt")
    classNames = ["Fire", "Smoke"]
    iterator = 0
    while True:
        iterator += 1
        print(iterator)
        is_detected = False
        success, img = cap.read()
        results = model(img, stream=True, imgsz=320, conf=0.5)
        for r in results:
            boxes = r.boxes
            for box in boxes:
                is_detected = True
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
                conf = math.ceil((box.conf[0] * 100)) / 100
                cls = int(box.cls[0])
                class_name = classNames[cls]
                label = f'{class_name}{conf}'
                t_size = cv2.getTextSize(label, 0, fontScale=1, thickness=2)[0]

                c2 = x1 + t_size[0], y1 - t_size[1] - 3
                cv2.rectangle(img, (x1, y1), c2, [255, 0, 255], -1, cv2.LINE_AA)  # filled
                cv2.putText(img, label, (x1, y1 - 2), 0, 1, [255, 255, 255], thickness=1, lineType=cv2.LINE_AA)
                if iterator >= 1000:
                    iterator = 0
                    alert_camera.set({
                        "id": str(camera_pk.pk) + camera_pk.camera_name,
                        "web_address": camera_pk.web_address,
                        "camera_id": camera_pk.pk,
                        "time": int(round(time.time() * 1000)),
                    }, merge=True)

        yield img
    # out.write(img)
    # cv2.imshow("image", img)
    # if cv2.waitKey(1) & 0xFF==ord('1'):
    # break
    # out.release()


cv2.destroyAllWindows()
