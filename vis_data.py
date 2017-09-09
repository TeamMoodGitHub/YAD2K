import cv2
from PIL import Image, ImageDraw
import numpy as np
from read_ocr_and_lolesport_data import get_game_data_dict

FRAME_DIR = "/Users/flynn/Documents/DeepLeague/data/DIG_CLG_G1_SEPT_1/frames/"

def main():
    # at this point, game_data has a dict of frame objects with a frame_path IF one was found for it.
    # game data's keys are in order of game time.
    game_data = get_game_data_dict()
    visualize_game_data(game_data)

def visualize_game_data(game_data):
    for time_stamp in game_data:
        frame_obj = game_data[time_stamp]
        # not all frame objs have actual frames asscoiated with them!
        if frame_obj.frame_path is not None:
            print("%s .... %s" % (frame_obj.time_obj.time_as_string, frame_obj.frame_path))
            x_val = int(frame_obj.game_snap['playerStats']['7']['x'])
            y_val = int(frame_obj.game_snap['playerStats']['7']['y'])

            x_val_2 = int(frame_obj.game_snap['playerStats']['2']['x'])
            y_val_2 = int(frame_obj.game_snap['playerStats']['2']['y'])

            # load in image w/ PIL for easy drawing / cropping
            im = Image.open(FRAME_DIR + frame_obj.frame_path).crop((1625, 785, 1920, 1080))
            draw = ImageDraw.Draw(im)
            draw.rectangle([(x_val - 19, y_val - 20),(x_val + 11, y_val + 10)], outline='red')
            draw.rectangle([(x_val_2 - 19, y_val_2 - 20),(x_val_2 + 11, y_val_2 + 10)], outline='blue')

            print("1 ", x_val - 19)
            print("2 ", y_val - 20)
            print("3 ", x_val + 11)
            print("4 ", y_val + 10)
            print('\n')
            # now draw using PIL
            del draw

            im = np.array(im, dtype = np.uint8)
            im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB )
            cv2.imshow("IMAGE", im)
            if cv2.waitKey(1) == ord('q'):
                break

if __name__ == "__main__":
    main()
