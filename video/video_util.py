#! /Users/sugar/.pyenv/versions/skrsugar/bin/python
"""
@File    :   video_util.py    
@Contact :   zhangyu@onesight.com

@Modify Time    @Author @Version    @Description
------------    ------- --------    -----------
2023/9/20       zhangyu 1.0         None
"""

import cv2
import random
import os
import sys

MB = 1024 * 1024
FACE_CLASSIER = cv2.CascadeClassifier(f'{cv2.data.haarcascades}/haarcascade_frontalface_default.xml')


def face_detect(cv2_image):
    # 灰度处理
    gray = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2GRAY)
    # 检测人脸
    faces = FACE_CLASSIER.detectMultiScale(gray, 1.1, 3)
    cv2.destroyAllWindows()
    return len(faces) > 0


def screen_shot(video_dir, screen_shot_path, size_filter=150 * MB):
    for fpathe, dirs, fs in os.walk(video_dir):
        for f in fs:
            video_path = os.path.join(fpathe, f)
            os.stat(video_path)
            video_file_name = video_path.split('/')[-1]
            if (not video_file_name.lower().endswith('.mp4')) or (os.stat(video_path).st_size < size_filter):
                continue
            cap = cv2.VideoCapture(video_path)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            face_counter, num_frames_to_capture = 0, 20

            while face_counter < 20:
                frame_indices = random.sample(range(frame_count), num_frames_to_capture)

                for index in frame_indices:
                    cap.set(cv2.CAP_PROP_POS_FRAMES, index)
                    ret, frame = cap.read()
                    if ret:
                        image_filename = f'{video_file_name}_screenshot_{index}.png'

                        # 设置水印文本和字体样式
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        font_scale = 1
                        font_thickness = 2
                        font_color = (0, 0, 255)  # 字体颜色 (BGR格式，这里是红色)
                        position = (50, 50)  # 水印位置，以左上角为起点

                        if face_detect(frame):
                            cv2.putText(frame, video_file_name, position, font, font_scale, font_color, font_thickness, cv2.LINE_AA)
                            cv2.imwrite(f'{screen_shot_path}/{image_filename}', frame)
                            print(f'Saved screenshot {index} at {screen_shot_path}/{image_filename}')
                            face_counter += 1
                            if face_counter >= 20:
                                break
                        else:
                            print('no face detected! skip screenshot')

            cap.release()
    os.system('osascript /Users/sugar/PycharmProjects/skrsugar/apple_scripts/openairdrop.applescript')


if __name__ == '__main__':
    screen_shot(sys.argv[1], '/Users/sugar/PycharmProjects/skrsugar/screenshots')
