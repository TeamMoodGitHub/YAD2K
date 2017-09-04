# this file takes data thrown by the lolesport websocket, and matches it with the actual VOD.
import json
import numpy as np
import cv2
import os
from pprint import pprint
import tesserocr
from PIL import Image
import pytesseract

import sys

import pyocr
import pyocr.builders

tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)
# The tools are returned in the recommended order of usage
tool = tools[0]
print("Will use tool '%s'" % (tool.get_name()))
# Ex: Will use tool 'libtesseract'

langs = tool.get_available_languages()
print("Available languages: %s" % ", ".join(langs))
lang = langs[0]
print("Will use lang '%s'" % (lang))
# Ex: Will use lang 'fra'
# Note that languages are NOT sorted in any way. Please refer
# to the system locale settings for the default language
# to use.

JSON_FILE = "/Users/flynn/Documents/DeepLeague/data/DIG_CLG_G1_SEPT_1/TRLH1-1002340073_g1.json"
VOD_FILE = "/Users/flynn/Documents/DeepLeague/data/DIG_CLG_G1_SEPT_1/dig_clg_game_1.mp4"
FRAMES_PATH = "/Users/flynn/Documents/DeepLeague/data/DIG_CLG_G1_SEPT_1/frames/"


def main():
    with open(JSON_FILE) as data:
        print("Parsing JSON. Might take a while depending on game length.")
        parsed_data = json.load(data)
        print("Done parsing JSON.")

        times = []
        for i in range(0, len(parsed_data)):
            times.append(parsed_data[i]['t'])
        times = np.asarray(times)
        times = np.around(times / 1000, 0)

        for i in range(1, len(times)):
            if(times[i-1] + 1 != times[i]):
                print("Time not consistent at time ", times[i])

        run_ocr_on_vod()

def run_ocr_on_vod():
    # first split the video up into frames with PIL, two frames per second is good for now.
    # frames = get_frames()-


    # PIL crop left, upper, right, and lower
    # on a 1920x180 video, time is located at (900, 75, 1000, 125)
    files = os.listdir(FRAMES_PATH)

    # only care about jpg frames.
    for file in files:
        if(file.split(".")[1] != "jpg"):
            files.remove(file)

    # trick to sort files in numerical order given format "frame_#.jpg"
    sorted_files = sorted(files, key=lambda x: int(x.split('_')[1].split(".")[0]))

    for file in sorted_files:
        print(file)
        # load in and crop gray scaled image
        frame = Image.open(FRAMES_PATH + file).convert('L')#.crop((956, 85, 975, 100))

        # convert to opencv format
        frame_cv = np.array(frame)
        # retval2,threshold2 = cv2.threshold(frame_cv,125,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        frame_cv = cv2.threshold(frame_cv, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        frame_cv = cv2.medianBlur(frame_cv, 3)
        # # back to PIL
        frame_pil = Image.fromarray(frame_cv)#.crop((956, 85, 975, 100))
        frame_pil.save("tst", "jpeg")
        print(pytesseract.image_to_string(frame_pil))
        # digits = tool.image_to_string(
        #     frame,
        #     lang=lang,
        #     builder=pyocr.tesseract.DigitBuilder()
        # )
        # print(digits)



if __name__ == "__main__":
    print("Started")
    main()
