import json
import cv2
from math import floor
import sys


# holds all data associated with a specifc frame
class Frame:
    def __init__(self, easy_time_obj, game_frame):
        self.time_obj = easy_time_obj
        self.game_frame = game_frame
        self.frame_path = None

# decided to write my own time class.
class EasyTime:
    def __init__(self, minutes, seconds):
        self.minutes = minutes
        self.seconds = seconds
        self.time_as_string = "%01d:%02d" % (minutes, seconds)

LOL_ESPORT_JSON = "/Users/flynn/Documents/DeepLeague/data/DIG_CLG_G1_SEPT_1/TRLH1-1002340073_g1.json"
TIMESTAMP_JSON = "/Users/flynn/Documents/DeepLeague/data/DIG_CLG_G1_SEPT_1/timestamp_data.json"

def main():
    # first load in lolesport JSON data. all we want is one time stamp at a time.

    full_game_data = json.load(open(LOL_ESPORT_JSON, 'r'))
    frame_timestamp_data = json.load(open(TIMESTAMP_JSON, 'r'))

    # TODO: work on func clean_data_for_bad_times(frame_timestamp_data)

    # we want to match the data from the lolesports json with the data from the OCR via timestamps
    new_full_game_data = {}

    # heres the lolesport data in dict where the key is the timestamp
    for full_frame in full_game_data:
        time_obj = convert_ms_to_easy_time(full_frame['t'])

        if time_obj.time_as_string not in new_full_game_data:
            new_full_game_data[time_obj.time_as_string] = Frame(time_obj, full_frame)

    # now use the OCR data to match up the proper image
    first = True
    for time_frame in frame_timestamp_data:
        if first:
            first = False
            continue
        time_obj = convert_string_time_to_easy_time(time_frame['time'])

        # once we have the time represented in the frame, we can match it with a frame object in new_full_game_data
        if time_obj.time_as_string in new_full_game_data:
            if new_full_game_data[time_obj.time_as_string].frame_path == None:
                new_full_game_data[time_obj.time_as_string].frame_path = time_frame['file_name']
                print(new_full_game_data[time_obj.time_as_string].frame_path)
                print(new_full_game_data[time_obj.time_as_string].time_obj.time_as_string)
                # print(new_full_game_data[time_obj.time_as_string].game_frame)

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
