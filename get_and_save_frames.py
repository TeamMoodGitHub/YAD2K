# takes a VOD, and outputs the frames. frames to campture per second can be adjusted.
# this program was made to run manually

import cv2
from PIL import Image
import numpy as np

INPUT_VOD_PATH = "/Users/flynn/Documents/DeepLeague/data/CLG_P1_G_3_MARCH_3_2017/vod.mp4"

vod_name_list = ['C9_FOX_G_2_MARCH_4_2017', 'CLG_TSM_G_1_MARCH_4_2017', 'CLG_TSM_G_2_MARCH_4_2017', 'DIG_P1_G_1_MARCH_4_2017', 'DIG_P1_G_2_MARCH_4_2017', 'DIG_P1_G_3_MARCH_4_2017', 'FLY_NV_G_1_MARCH_4_2017', 'FLY_NV_G_2_MARCH_4_2017', 'FLY_NV_G_3_MARCH_4_2017', ]

def get_frames():

    for file_path in vod_name_list:
        video = cv2.VideoCapture('data/%s/vod.mp4' % file_path)
        print("Currently on ", file_path)
        # forward over to the frames you want to start reading from.
        # manually set this, fps * time in seconds you wanna start from
        video.set(1, 0);
        success, frame = video.read()
        count = 0
        file_count = 0
        success = True
        fps = int(video.get(cv2.CAP_PROP_FPS))
        total_frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        print("Loading video %d seconds long with FPS %d and total frame count %d " % (total_frame_count/fps, fps, total_frame_count))

        while success:
            success, frame = video.read()
            if not success:
                break
            if count % 1000 == 0:
                print("Currently at frame ", count)

            # i save once every fps, which comes out to 1 frames per second.
            # i think anymore than 2 FPS leads to to much repeat data.
            if count %  fps == 0:
                im = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                im = Image.fromarray(frame)
                im = np.array(im, dtype = np.uint8)
                cv2.imwrite("data/%s/frames/frame_%d.jpg" %  (file_path, file_count), im)
                file_count += 1
            count += 1

        print("Saved %d frames" % (file_count) )
        video.release()


if __name__ == "__main__":
    get_frames()
