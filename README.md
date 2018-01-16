# DeepLeague - by Farza  

### How do I get DeepLeague?
All you need to get going in is [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git), [Python 3.6](https://www.python.org/downloads/), and [conda](https://conda.io/docs/user-guide/install/index.html) (you'll need to download them in this order!). Once you install them you can check if everything works okay by typing in these commands in your terminal. 

```sh
$ python
$ conda
$ git
```

If you were able to run those three commands without any errors, you can continue.
```sh
$ git clone --recursive https://github.com/farzaa/DeepLeague.git
$ cd DeepLeague
$ cd YAD2K
$ conda create --name DeepLeague
$ source activate DeepLeague

$ pip install opencv-python
$ pip install youtube_dl
$ conda install -c menpo ffmpeg
$ pip install numpy h5py pillow
$ pip install tensorflow-gpu
$ pip install keras

$ wget http://pjreddie.com/media/files/yolo.weights
$ wget https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolo.cfg
$ python yad2k.py yolo.cfg yolo.weights model_data/yolo.h5
```

You are almost good to go. Last thing you need is the file for the weights:
https://drive.google.com/open?id=1-r_4Ex3OC-MTcTwNE7xJkdpiSz_3rb8A

Download this and put it in the YAD2K diretory. The script will expect it to be here.


### How do I run DeepLeague?
Honestly, this repo has so many tiny fucntions. But, let me explain the easiest way to get this going if all you want to do is analyze a VOD (which most of you want I presume). the test_deep_league.py is the key to running everything. Its a little command line tool I made that lets you input a VOD to analyze in three different ways: a YouTube link, path to local MP4, path to a directory of images. I like the YouTube link option best, but if you have trouble with it feel free to use the MP4 approach instead. All you need is a 1080P VOD of a League game.

Heres an example of me running the tool with a YouTube link. This method automatically downloads the YT video as well and cuts it up according to the the start and end time you gave it. It will automatically do all the renaming to process stuff. Nice! This command specifies to start at the 30 second mark and end 1 minute in.
```sh
python test_deep_league.py -out output youtube -yt https://www.youtube.com/watch?v=vPwZW1FvtWA -yt_path /output -start 0:00:30 -end 0:01:00
```

Here's an example of me running the tool with an MP4

```sh
python test_deep_league.py -out output mp4 -mp4 /Volumes/DATA/data/data/C9_CLG_G_2_MARCH_12_2017/vod.mp4
```


