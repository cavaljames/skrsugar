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


def screen_shot(video_path, screen_shot_path):
    video_file_name = video_path.split('/')[-1]
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    num_frames_to_capture = 20
    frame_indices = random.sample(range(frame_count), num_frames_to_capture)

    for index in frame_indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, index)
        ret, frame = cap.read()
        if ret:
            image_filename = f'screenshot_{index}.png'

            # 设置水印文本和字体样式
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1
            font_thickness = 2
            font_color = (0, 0, 255)  # 字体颜色 (BGR格式，这里是红色)
            position = (50, 50)  # 水印位置，以左上角为起点

            cv2.putText(frame, video_file_name, position, font, font_scale, font_color, font_thickness, cv2.LINE_AA)
            cv2.imwrite(f'{screen_shot_path}/{image_filename}', frame)

            print(f'Saved screenshot {index} at {screen_shot_path}/{image_filename}')

    cap.release()
    os.system('osascript /Users/sugar/PycharmProjects/skrsugar/apple_scripts/openairdrop.applescript')


if __name__ == '__main__':
    import sys
    screen_shot(sys.argv[1], '/Users/sugar/PycharmProjects/skrsugar/screenshot')
