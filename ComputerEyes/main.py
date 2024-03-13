import asyncio
import datetime
import os.path
from threading import Thread

import cv2
import pandas as pd
import numpy as np
from IPython.core.display_functions import display
from ultralytics import YOLO
import torch
from IPython.display import clear_output
from PIL import Image

from yolo_detect import Video, CustomYOLODetect


def main() -> None:
    model = YOLO('yolov8s.pt')

    print(f"Using Torch {torch.__version__}\n"
          f" ({torch.cuda.get_device_properties(0).name if torch.cuda.is_available() else 'CPU'})")

    # print(Video(video_path='video/test.avi'))

    with open('coco.txt', 'r', encoding='utf-8') as f:
        data = f.read()
    class_list = data.split('\n')
    print(class_list)
    count = 0

    # area = [(381, 104), (342, 125), (599, 192), (597, 151)]
    # area [(LD), (LU), (RU), (RD)]. L -> Left, R -> Right, U -> Up, D -> Down
    #               236,51
    # area = [(86, 102), (228, 60), (300, 66), (574, 74), (460, 172)]
    # area [(LD), (LU), (LUR), (RU), (URD), (RD), (RDL)]
    # area = [(120, 102), (190, 50), (342, 65), (574, 80), (558, 132), (458, 179), (281, 125)]
    area = [(700, 202), (770, 130), (890, 145), (800, 240)]
    # cap = cv2.VideoCapture('video/test.avi')
    cap = cv2.VideoCapture("rtsp://admin:zer0vide0@192.168.6.6/")
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    # path_workdir = datetime.datetime.now().strftime("%Y_%m_%d")
    # path = datetime.datetime.now().strftime("%H_%M")
    # if not os.path.exists(f'video/{path_workdir}'):
    #     os.mkdir(f'video/{path_workdir}')
    # out = cv2.VideoWriter(
    #     f'video/{path_workdir}/output_{path}.mp4', fourcc, 60.0,
    #     (1020,
    #      500))

    # Loop over the frames of the video
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        count += 1

        # Process every third frame to reduce processing load
        if count % 3 != 0:
            continue
        # Skip frames with no data
        if frame is None or frame.shape[0] == 0 or frame.shape[1] == 0:
            continue
        # Resize the frame for faster processing
        frame = cv2.resize(frame, (1020, 500))
        # frame = cv2.resize(frame, (1920, 1080))
        # Predict the objects in the frame with YOLO model
        results = model.predict(frame)
        a = results[0].boxes.data
        px = pd.DataFrame(a.cpu().numpy()).astype('float')
        car_list = []
        # Loop over the detected objects
        for index, row in px.iterrows():
            x1 = int(row[0])
            y1 = int(row[1])
            x2 = int(row[2])
            y2 = int(row[3])
            d = int(row[5])
            c = class_list[d]

            # Check if the detected object is a car and is inside the area of interest
            if 'car' in c:
                cx = int(x1 + x2) // 2
                cy = int(y1 + y2) // 2
                results = cv2.pointPolygonTest(np.array(area, np.int32), ((cx, cy)), False)
                if results >= 0:
                    # Draw a rectangle around the car, a circle on its centroid, and its class name
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.circle(frame, (cx, cy), 4, (255, 0, 255), -1)
                    cv2.putText(frame, str(c), (x1, y1), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0), 1)
                    car_list.append([c])
        # Draw the area of interest polygon and the number of detected cars in the frame
        cv2.polylines(frame, [np.array(area, np.int32)], True, (255, 0, 2), 2)
        k = len(car_list)
        cv2.putText(frame, str(k), (50, 60), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 3)
        cv2.imshow('Video', frame)
        clear_output(wait=True)
        display(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
        # out.write(frame)
        # Exit the loop when 'ESC' key is pressed
        if cv2.waitKey(1) & 0xFF == 27:
            break
    # Release the video file and close all windows
    cap.release()
    # out.release()
    cv2.destroyAllWindows()


async def sec():
    
    custom_yolo = CustomYOLODetect(

        model="yolov8s.pt",
        areas="right",
        cap=cv2.VideoCapture("rtsp://admin:zer0vide0@192.168.6.6/")
    )
    custom_yolo_sec = CustomYOLODetect(
        model="yolov8s.pt",
        areas="left",
        model='yolov8s.pt',
        areas='right',
        cap=cv2.VideoCapture("rtsp://admin:zer0vide0@192.168.6.6/")
    )
    custom_yolo_sec = CustomYOLODetect(
        model='yolov8s.pt',
        areas='left',

        cap = cv2.VideoCapture("rtsp://admin:zer0vide0@192.168.6.6/")
    )
    # thread_left = Thread(target=await custom_yolo.run(False, True))
    # thread_right = Thread(target=await custom_yolo_sec.run(False, True))
    # thread_left.start()
    # thread_right.start()

    # thread_left.join()
    # thread_right.join()
    await custom_yolo.run(False, True)
    await custom_yolo_sec.run(False, True)

async def detect_car_on_out():
    custom_yolo = CustomYOLODetect(
        model="yolov8s.pt",
        areas="out",
        cap=cv2.VideoCapture("rtsp://admin:zer0vide0@192.168.6.6/"),
    )
    
    await custom_yolo.run(False, True)

if __name__ == '__main__':

    import sys

    if (sys.argv):
        asyncio.run(detect_car_on_out())
    else:
        asyncio.run(sec())
