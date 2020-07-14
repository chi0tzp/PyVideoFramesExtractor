# PyVideoFramesExtractor: Extract frames from videos in Python using OpenCV

Extract frames from a single video file or from all video files under a given directory (including all its sub-directories). Extracted frames are stored under a given output directory keeping the structure of the original directory (when a video directory is given, instead of a single video file).

## Usage

~~~bash
python extract.py -h
usage: Extract frames from videos [-h] [--video VIDEO | --dir DIR] [--sampling SAMPLING]                                       [--output_root OUTPUT_ROOT] [--workers WORKERS]

optional arguments:
      -h, --help            show this help message and exit
      --video VIDEO         set video filename
      --dir DIR             set videos directory
      --sampling SAMPLING   extract 1 frame every args.sampling seconds                                                 (default: extract all frames)
  --output_root OUTPUT_ROOT
                            set output root directory
  --workers WORKERS         Set number of multiprocessing workers
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
python extract.py --video=demo_videos/talking_dog.mp4
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
python extract.py --dir=demo_videos/
#. Extract frames from videos under dir : demo_videos/
#. Store extracted frames under         : extracted_frames
#. Extract all available frames.
#. Scan for video files...
100%|███████████████████████████████████████████████████| 3/3 [00:47<00:00, 15.94s/it]
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

