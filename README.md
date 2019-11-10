# PyVideoFramesExtractor: Extract frames from videos in Python using OpenCV

Extract frames from a single video file or from all video files under a given directory (including all its sub-directories). Extracted frames are stored under a given output directory keeping the structure of the original directory (when a video directory is given, instead of a single video file).

## Usage

~~~bash
python extract.py -h
usage: Extract frames from videos [-h] [-o OUTPUT_ROOT] [-q]
                                  [-v VIDEO | -d DIR]

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_ROOT, --output_root OUTPUT_ROOT
                        set output root directory
  -q, --quite           set quite mode on
  -v VIDEO, --video VIDEO
                        set video filename
  -d DIR, --dir DIR     set videos directory
~~~



## Demo

Directory `demo_videos` contains three videos downloaded from YouTube videos under the **Creative Commons Attribution license**:

~~~
demo_videos/
├── talking_dog.mp4 (https://www.youtube.com/watch?v=1oR6-982NHY)
└── video_dir
    ├── michael_haneke.mp4 (https://www.youtube.com/watch?v=ULzjUUYWge4)
    └── techno_viking.mp4 (https://www.youtube.com/watch?v=Y1tKRQ5Msc0)
~~~



### Extract frames from a single video file

~~~
python extract.py -v=demo_videos/talking_dog.mp4
#. Extract frames from video file: demo_videos/talking_dog.mp4
  \__Video FPS    : 29.97002997002997
  \__Video length : 2418 (frames)
  \__Progress     : ████████████████████ 100% 

~~~

Extracted frames are stored under `extracted_frames/demo_videos/talking_dog_frames/` as follows:

~~~
extracted_frames/demo_videos/talking_dog_frames/
├── 00000001.jpg
├── 00000002.jpg
├── 00000003.jpg
├── ...
├── 00002416.jpg
├── 00002417.jpg
└── 00002418.jpg

0 directories, 2418 files
~~~



### Extract frames from a directory of video files

~~~
python extract.py -d=demo_videos/
#. Extract frames from videos in directory : demo_videos/
#. Store extracted frames under            : extracted_frames
#. Scan for video files...
#. Extract frames from video file: demo_videos/talking_dog.mp4
  \__Video FPS    : 29.97002997002997
  \__Video length : 2418 (frames)
  \__Progress     : ████████████████████ 100% 

#. Extract frames from video file: demo_videos/video_dir/michael_haneke.mp4
  \__Video FPS    : 23.976023976023978
  \__Video length : 3832 (frames)
  \__Progress     : ████████████████████ 100% 

#. Extract frames from video file: demo_videos/video_dir/techno_viking.mp4
  \__Video FPS    : 25.0
  \__Video length : 6024 (frames)
  \__Progress     : ████████████████████ 100%
~~~

Extracted frames are stored under `extracted_frames/` as follows:

~~~
extracted_frames/
└── demo_videos
    ├── talking_dog_frames
    │   ├── 00000001.jpg
    │   ├── 00000002.jpg
    │   ├── 00000003.jpg
    │   ├── ...
    │   ├── 00002416.jpg
    │   ├── 00002417.jpg
    │   └── 00002418.jpg
    └── video_dir
        ├── michael_haneke_frames
        │   ├── 00000001.jpg
        │   ├── 00000002.jpg
        │   ├── 00000003.jpg
        │   ├── ...
        │   ├── 00003830.jpg
        │   ├── 00003831.jpg
        │   └── 00003832.jpg
        └── techno_viking_frames
            ├── 00000001.jpg
            ├── 00000002.jpg
            ├── 00000003.jpg
            ├── ...
            ├── 00006022.jpg
            ├── 00006023.jpg
            └── 00006024.jpg

5 directories, 12274 files
~~~

