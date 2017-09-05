import json
import cv2
from math import floor
import sys
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from file_fixer import sort_files_numerically
from pprint import pprint
from PIL import Image
import numpy as np

# holds all data associated with a specifc frame
class Frame:
    def __init__(self, easy_time_obj, game_snap):
        self.time_obj = easy_time_obj
        self.game_snap = game_snap
        self.frame_path = None

# decided to write my own time class.
class EasyTime:
    def __init__(self, minutes, seconds):
        self.minutes = minutes
        self.seconds = seconds
        self.time_as_string = "%01d:%02d" % (minutes, seconds)

LOL_ESPORT_JSON = "/Users/flynn/Documents/DeepLeague/data/DIG_CLG_G1_SEPT_1/TRLH1-1002340073_g1.json"
TIMESTAMP_JSON = "/Users/flynn/Documents/DeepLeague/data/DIG_CLG_G1_SEPT_1/timestamp_data.json"
FRAME_DIR = "/Users/flynn/Documents/DeepLeague/data/DIG_CLG_G1_SEPT_1/frames/"

def main():
    # at this point, game_data has a dict of frame objects with a frame_path IF one was found for it.
    # game data's keys are in order of game time.
    game_data = create_data()
    rescale_coordinates(game_data)
    visualize_game_data(game_data)


def visualize_game_data(game_data):
    plt.ion()
    fig, ax = plt.subplots(1)


    for time_stamp in game_data:
        frame_obj = game_data[time_stamp]
        # not all frame objs have actual frames asscoiated with them!
        if frame_obj.frame_path is not None:

            print("%s .... %s" % (frame_obj.time_obj.time_as_string, frame_obj.frame_path))
            # read in for matplotlib and crop just the map 1625, 785, 1920, 1080
            im = np.array(Image.open(FRAME_DIR + frame_obj.frame_path).crop((1625, 785, 1920, 1080)), dtype=np.uint8)
            img = ax.imshow(im)
            x_val = int(frame_obj.game_snap['playerStats']['7']['x'])
            y_val = int(frame_obj.game_snap['playerStats']['7']['y'])

            rect = patches.Rectangle((x_val - 15, y_val - 20), 30, 30, linewidth=2, edgecolor='r', facecolor='none')
            ax.add_patch(rect)


            plt.pause(.01)
            plt.draw()

            rect.remove()


def create_data():
    # first load in lolesport JSON data. all we want is one time stamp at a time.
    full_game_data = json.load(open(LOL_ESPORT_JSON, 'r'))
    frame_timestamp_data = json.load(open(TIMESTAMP_JSON, 'r'))

    # we want to match the data from the lolesports json with the data from the OCR via timestamps
    new_full_game_data = {}

    # heres the lolesport data is in new_full_game_data where the key is the timestamp
    for full_frame in full_game_data:
        time_obj = convert_ms_to_easy_time(full_frame['t'])
        print(time_obj.time_as_string)
        # in this case every single game snap turns into a Frame object.
        # but not every game snap will be associated with a Frame.frame_path
        if time_obj.time_as_string not in new_full_game_data:
            new_full_game_data[time_obj.time_as_string] = Frame(time_obj, full_frame)


    # now use the OCR data to match up the Frame objects with the proper frame_path
    first = True
    for time_frame in frame_timestamp_data:
        # skip over first item in json
        if first:
            first = False
            continue

        # using json data created by ocr, figure out the time of the game time of the current real game image
        time_obj = convert_string_time_to_easy_time(time_frame['time'])
        # only keep game frame if it has a game_snap associated with it.
        if time_obj.time_as_string in new_full_game_data:
            # only keep game frame if it has an actual frame associated with it
            if new_full_game_data[time_obj.time_as_string].frame_path == None:
                new_full_game_data[time_obj.time_as_string].frame_path = time_frame['file_name']

    return new_full_game_data

def convert_ms_to_easy_time(time_in):
    full_time_in_seconds = floor(time_in / 1000)
    minutes = floor(full_time_in_seconds / 60)
    seconds = full_time_in_seconds - minutes * 60
    return EasyTime(minutes, seconds)

def convert_string_time_to_easy_time(time_str):
    minutes, seconds = time_str.split(":")
    time_obj = EasyTime(int(minutes), int(seconds))

    # just as a sanity check
    if time_obj.time_as_string != time_str:
        print("JSON time does not equal calculated time")
        print(time_str)
        print(time_obj.time_as_string)
        sys.exit(1)

    return time_obj

def rescale_coordinates(game_data):

    x = [int(game_data[t].game_snap['playerStats']['7']['x']) for t in game_data]
    y = [int(game_data[t].game_snap['playerStats']['7']['y']) for t in game_data]
    # first calculate max/min for x/y
    # for time_stamp in game_data:
    #     frame_obj = game_data[time_stamp]
    #     # not all frame objs have actual frames asscoiated with them!
    #     x.append(int(frame_obj.game_snap['playerStats']['7']['x']))
    #     y.append(int(frame_obj.game_snap['playerStats']['7']['y']))

    x_old_min = min(x)
    x_old_max = max(x)
    y_old_min = min(y)
    y_old_max = max(y)

    x_new_max = 270
    x_new_min = 20

    y_new_max = 20
    y_new_min = 270

    for time_stamp in game_data:
        old_x = game_data[time_stamp].game_snap['playerStats']['7']['x']
        old_y = game_data[time_stamp].game_snap['playerStats']['7']['y']

        game_data[time_stamp].game_snap['playerStats']['7']['x'] = (((old_x - x_old_min) * (x_new_max - x_new_min)) / (x_old_max - x_old_min)) + x_new_min
        game_data[time_stamp].game_snap['playerStats']['7']['y'] = (((old_y - y_old_min) * (y_new_max - y_new_min)) / (y_old_max - y_old_min)) + y_new_min

    return game_data
    # now we can calculate new coordinates



    (((old_val - old_min) * (new_max - new_min)) / (old_max - old_min)) + new_min

# TODO below!
# sometimes ocr will return times that aren't in sync
# i mostly see this issue with double digits
# for example, it can return 10:39, then 0:39 because it missed the full 10
# to fix this, i run this method.
def clean_data_for_bad_times(frame_timestamp_data):
    prev_time = None
    first = True
    for time_frame in frame_timestamp_data:
        if first:
            first = False
            continue
        if prev_time is None:
            prev_time = convert_string_time_to_easy_time(time_frame['time'])
            continue
        curr_time = convert_string_time_to_easy_time(time_frame['time'])
        print(curr_time.time_as_string)
        # its impossible for the minutes from a previous frame to be bigger than the curr!

        if prev_time.minutes > curr_time.minutes:
            print("KICKING")
            del frame_timestamp_data[time_frame]


        prev_time = curr_time




if __name__ == "__main__":
    main()
