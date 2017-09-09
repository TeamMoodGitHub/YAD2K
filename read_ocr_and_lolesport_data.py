import json
import cv2
from math import floor
import sys
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from file_fixer import sort_files_numerically
from pprint import pprint
from PIL import Image, ImageDraw
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

LOL_ESPORT_JSON = "/Users/flynn/Documents/DeepLeague/data/DIG_CLG_G1_SEPT_1/game_1.json"
TIMESTAMP_JSON = "/Users/flynn/Documents/DeepLeague/data/DIG_CLG_G1_SEPT_1/time_stamp_data_clean.json"
FRAME_DIR = "/Users/flynn/Documents/DeepLeague/data/DIG_CLG_G1_SEPT_1/frames/"


champs_to_look_for = ['2', '7']

def get_game_data_dict():
    game_data = create_data()
    rescale_coordinates(game_data)
    remove_dead_times(game_data)
    return game_data

def create_data():
    # first load in lolesport JSON data. all we want is one time stamp at a time.
    full_game_data = json.load(open(LOL_ESPORT_JSON, 'r'))
    frame_timestamp_data = json.load(open(TIMESTAMP_JSON, 'r'))

    # we want to match the data from the lolesports json with the data from the OCR via timestamps
    new_full_game_data = {}

    # heres the lolesport data is in new_full_game_data where the key is the timestamp
    for full_frame in full_game_data:
        time_obj = convert_ms_to_easy_time(full_frame['t'])
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
    # these numbers are from remixz on GitHub, not sure how he got them, but they work!
    x_old_min = -120
    x_old_max = 14870
    y_old_min = -120
    y_old_max = 14980

    # got these by trial and error. they just "shrink" down the map by 5 px on each side.
    # helps cut some of the edges off.

    x_new_max = 290
    x_new_min = 5

    y_new_max = 5
    y_new_min = 290

    for champ_num in champs_to_look_for:
        for time_stamp in game_data:
            old_x = game_data[time_stamp].game_snap['playerStats'][champ_num]['x']
            old_y = game_data[time_stamp].game_snap['playerStats'][champ_num]['y']

            game_data[time_stamp].game_snap['playerStats'][champ_num]['x'] = (((old_x - x_old_min) * (x_new_max - x_new_min)) / (x_old_max - x_old_min)) + x_new_min
            game_data[time_stamp].game_snap['playerStats'][champ_num]['y'] = (((old_y - y_old_min) * (y_new_max - y_new_min)) / (y_old_max - y_old_min)) + y_new_min

    return game_data

# we want to remove the frames where the champs is dead, but still has a position
# this is useless data because it doesn't show the champs image on the minimap when the champ's dead
# TODO
# what i do is set the champs x and y to 0, 0 if they are dead
# this way i can handle it as a special case later
def remove_dead_times(game_data):
    keys_to_remove = []
    for champ_num in champs_to_look_for:
        for time_stamp in game_data:
            hp = game_data[time_stamp].game_snap['playerStats'][champ_num]['h']
            # dead when HP is 0
            if hp == 0:
                print("%s dead at %s" %(champ_num, time_stamp))
                game_data[time_stamp].game_snap['playerStats'][champ_num]['x'] = 0
                game_data[time_stamp].game_snap['playerStats'][champ_num]['y'] = 0

if __name__ == "__main__":
    get_game_data_dict()
