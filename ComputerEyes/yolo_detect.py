import json
import os
from datetime import timedelta, datetime
from pathlib import Path
from time import sleep
from typing import Union, Any

import cv2
import numpy as np
import pandas as pd
import supervision as sv
from IPython.core.display_functions import display
from IPython.display import clear_output
from PIL import Image
from beartype import beartype
from beartype.typing import List, Dict, Tuple
from ultralytics import YOLO
import logging


@beartype
class Video:

    def __init__(self, video_path: str) -> None:
        self.video_path: str = video_path
        self.video_info: sv.VideoInfo = sv.VideoInfo.from_video_path(self.video_path)
        self.__build_params()

    def __build_params(self) -> None:
        self.width: int = self.video_info.width
        self.height: int = self.video_info.height
        self.fps: int = self.video_info.fps
        self.total_frames: int = self.video_info.total_frames
        self.length: timedelta = timedelta(seconds=round(self.total_frames / self.fps))

    def __str__(self) -> str:
        return f"033[1mVideo Resolution:\033[0m ({self.width}, {self.height})\n" \
               f"\033[1mFPS:\033[0m {self.fps}\n" \
               f"\033[1mLength:\033[0m {self.length}"


def save_output_on_json(value_to_save: int, area: str = 'right') -> None:
    logging.warning(F"JSON: {value_to_save} | {area}")
    logging.warning(F"PAth: {os.path.abspath(__file__)}")
    if not os.path.exists(f'outputs_{area}.json'):
        with open(f'outputs_{area}.json', 'w', encoding='utf-8') as f:
            logging.warning(F"JSON PATH: {os.path.abspath(f)}")
            json.dump({
                area: 0
            }, f, indent=4, ensure_ascii=False)
    with open(f'outputs_{area}.json', 'r', encoding='utf-8') as f:
        obj = json.load(f)
        obj[area] = value_to_save
    with open(f'outputs_{area}.json', 'w', encoding='utf-8') as f:
        json.dump(obj, f, indent=4, ensure_ascii=False)


@beartype
class CustomYOLODetect:

    def __init__(self, model: Union[Path, str], task: Any = None,
                 dataset: Union[Path, str] = 'coco.txt',
                 videos_path: Union[str, None] = None,
                 required_videos: bool = False,
                 areas: str = 'right', cap: cv2.VideoCapture | None = None) -> None:
        sleep(10)
        self.areas: str = areas
        self._cached_: Dict = {}
        self.capture: cv2.VideoCapture | None = cap

        if required_videos:
            if videos_path is None:
                videos_path = 'video/test.avi'

            self.videos_path = videos_path

        self.model = YOLO(model, task)

        if not os.path.exists(dataset):
            with open(dataset, 'w', encoding='utf-8') as f:
                f.write("car \n person")
        with open(dataset, 'r', encoding='utf-8') as f:
            self.data: str = f.read()
        self.required_classes: List = self.data.strip().split('\n')
        
        self.count_area: Dict = {
            areas: 0 
        }
        # save_output_on_json(0, areas)

    @property
    def detection_areas(self):
        detection_areas = self._cached_.get('detection_areas')
        if not detection_areas:
            self.detection_areas = None
        return self._cached_['detection_areas']

    @detection_areas.setter
    def detection_areas(self, value: Union[Dict[str, List[Tuple]], None] = None):
        if value:
            self._cached_['detection_areas'] = value
            return
        self._cached_['detection_areas'] = {
            'right': [(120, 102), (190, 50), (342, 65), (574, 80), (558, 132), (458, 179), (281, 125)],
            'left': [(700, 202), (770, 130), (890, 145), (800, 240)],
            # 'out':[(450, 300), (550, 160), (650, 220), (410, 190)]
        }

    @property
    def fourcc(self):
        _fourcc_ = self._cached_.get('fourcc')
        if not _fourcc_:
            self.fourcc = 'mp4v'
        return self._cached_['fourcc']

    @fourcc.setter
    def fourcc(self, value):
        self._cached_['fourcc'] = cv2.VideoWriter_fourcc(*value)

    @property
    def output(self):
        return self._cached_.get('output')

    @output.setter
    def output(self, value):
        self._cached_['output'] = cv2.VideoWriter(
            value,
            self.fourcc,
            60.0,
            (1020, 500)
        )

    @property
    def out_path(self):
        return self._cached_.get('out_path')

    @out_path.setter
    def out_path(self, value):
        self._cached_['out_path'] = value if value else {
            'workdir': datetime.now().strftime("%Y_%m_%d"),
            'path': datetime.now().strftime("%H_%M")
        }

    @property
    def videos(self):
        _videos_ = self._cached_.get('videos')
        if not _videos_:
            self.videos = self.videos_path
        return self._cached_['videos']

    @videos.setter
    def videos(self, value):
        self._cached_['videos'] = cv2.VideoCapture(value)

    def build_output(self) -> None:
        self.out_path = None
        _out_ = self.out_path
        if not os.path.exists(f'video/{_out_["workdir"]}'):
            os.mkdir(f'video/{_out_["workdir"]}')

        self.output = f'video/{_out_["workdir"]}/{_out_["path"]}.mp4'

    def detection_thread(self, output_is_enabled: bool = False) -> None:
        print(f'{self.areas} Side \n\n\n\n\n\n')
        local_cache: Dict[str, Any] = {
            "sec": 0,
            "cars": []
        }

        count: int = 0
        cap: Any = self.capture
        # cap.open()
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            count += 1

            if count % 3 != 0:
                continue
            if frame is None or frame.shape[0] == 0 or frame.shape[1] == 0:
                continue
            frame = cv2.resize(frame, (1020, 500))

            results = self.model.predict(frame)
            a = results[0].boxes.data
            px = pd.DataFrame(a.cpu().numpy()).astype('float')
            car_list: List = []

            for index, row in px.iterrows():
                x1 = int(row[0])
                y1 = int(row[1])
                x2 = int(row[2])
                y2 = int(row[3])
                d = int(row[5])
                try:
                    c = self.required_classes[d]
                except Exception as ex:
                    print(ex)
                    continue
                if 'car' in c:
                    cx = int(x1 + x2) // 2
                    cy = int(y1 + y2) // 2
                    results = cv2.pointPolygonTest(np.array(self.detection_areas[self.areas], np.int32),
                                                   ((cx, cy)), False)
                    # logging.warning(F"RESULT: {results}")
                    if results >= 0:
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.circle(frame, (cx, cy), 4, (255, 0, 255), -1)
                        cv2.putText(frame, str(c), (x1, y1), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0), 1)
                        car_list.append([c])
            cv2.polylines(frame, [np.array(self.detection_areas[self.areas], np.int32)],
                          True, (255, 0, 2), 2)
            k = len(car_list)
            logging.warning(F"CARS: {k}")
            if k == 0:
                self.count_area[self.areas] = k
                save_output_on_json(self.count_area[self.areas], self.areas)
                break  
            local_cache['cars'].append(k)
            
            cv2.putText(frame, f"{str(k)}/15", (50, 60), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 3)
            cv2.imshow('Video', frame)
            # sleep(30)
            clear_output(wait=True)
            # display(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            # self.output.write(frame)
            # Exit the loop when 'ESC' key is pressed
            if cv2.waitKey(1) & 0xFF == 27:
                break
            if local_cache['sec'] >= 10:
                local_cache['sec'] = 0
                self.count_area[self.areas] = max(local_cache['cars'])
                print(F"{self.areas} | {self.count_area[self.areas]}")
                save_output_on_json(self.count_area[self.areas], self.areas)
                break   
            sleep(0.5)
            local_cache['sec'] += 1

        cap.release()
        if output_is_enabled:
            self.output.release()
        cv2.destroyAllWindows()

    async def run(self, required_outputs: bool = False, cap: bool = False) -> None:
        if required_outputs:
            self.build_output()
        if not cap:
            self.capture = self.videos
        # while True:
        self.detection_thread()
            # sleep(3600)
