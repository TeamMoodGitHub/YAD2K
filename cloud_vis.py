# calls Google Vision API to do OCR, and saved results to a CSV.
# i use the API vs Tesseract for performance reasons.
# credit for orignal program i altered - https://gist.github.com/dannguyen/a0b69c84ebc00c54c94d



import base64
from io import BytesIO
from os import makedirs
from os.path import join, basename
import json
import requests
import os
from PIL import Image
from pprint import pprint
import re


ENDPOINT_URL = 'https://vision.googleapis.com/v1/images:annotate'
RESULTS_DIR = 'jsons'
makedirs(RESULTS_DIR, exist_ok=True)

API_KEY = "AIzaSyDt5t0HpwXAidYtYA7PFGtCdPfgWclCKEQ"
IMAGE_DIR = "/Users/flynn/Documents/DeepLeague/data/DIG_CLG_G1_SEPT_1/frames/"
GAME_NAME = "DIG CLG SEPT 2"

def make_image_data_list(image_filenames):
    """
    image_filenames is a list of filename strings
    Returns a list of dicts formatted as the Vision API
        needs them to be
    """
    img_requests = []
    for imgname in image_filenames:
        # load as PIL
        img = Image.open(IMAGE_DIR + imgname).crop((900, 75, 1000, 125))
        buffer_str = BytesIO()
        img.save(buffer_str, 'jpeg')
        # convert to base64 for api
        encoded_string = base64.b64encode(buffer_str.getvalue()).decode()
        img_requests.append({
                'image': {'content': encoded_string},
                'features': [{
                    'type': 'TEXT_DETECTION',
                    'maxResults': 1
                }]
        })
    return img_requests

def make_image_data(image_filenames):
    """Returns the image data lists as bytes"""
    imgdict = make_image_data_list(image_filenames)
    return json.dumps({"requests": imgdict }).encode()


def request_ocr(api_key, image_filenames):
    response = requests.post(ENDPOINT_URL,
                             data=make_image_data(image_filenames),
                             params={'key': api_key},
                             headers={'Content-Type': 'application/json'})
    return response


if __name__ == '__main__':
    # get file paths
    image_paths = os.listdir(IMAGE_DIR)

    # only care about jpg frames.
    for file in image_paths:
        if(file.split(".")[1] != "jpg"):
            image_paths.remove(file)

    # sort in numerical order
    sorted_files = sorted(image_paths, key=lambda x: int(x.split('_')[1].split(".")[0]))
    # file we will write all data to
    outfile = open('data.json', 'w')
    outfile.write('[\n')
    json.dump({'info': GAME_NAME}, outfile)
    outfile.write(',\n')



    sys.exit(1)

    # regex for times
    reg = re.compile('^[0-5]?[0-9]:[0-9][0-9]$')
    # we only want to process 15 images per request to keep things organized
    for i in range(0, len(sorted_files) - 5, 5):
        # create list of images paths to send to api
        image_paths = []
        for j in range(0, 5):
            image_paths.append(sorted_files[i + j])
        print(image_paths)
        response = request_ocr(API_KEY, image_paths)

        if response.status_code != 200 or response.json().get('error'):
            print(response.text)
        else:

            for idx, resp in enumerate(response.json()['responses']):
                # save to JSON file
                print('--------------------------------------------------')

                if "textAnnotations" not in resp:
                    continue

                t = resp['textAnnotations'][0]
                time = t['description'].strip()
                imgname = sorted_files[i + idx]
                print(imgname)

                # check if time is in the proper format
                if reg.match(time) is None:
                    continue
                # create json objct to save data

                # TODO Check curr_time with prev_time to make sure OCR didn't mess up badly.
                obj = {'file_name': imgname, 'time': time}
                print(t['description'])
                json.dump(obj, outfile)
                outfile.write(',\n')


    outfile.write(']\n')
    outfile.close()
