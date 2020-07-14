import sys
import os
from os import walk
import os.path as osp
import argparse
import cv2
import math

# TODO: add additional supported video formats
supported_video_ext = ('.avi', '.mp4')

# TODO: add additional supported extracted frame formats
supported_frame_ext = ('.jpg', '.png')


class FrameExtractor:
    def __init__(self, video_file, output_dir, frame_ext='.jpg', sampling=-1, verbose=False):
        """Extract frames from video file and save them under a given output directory.

        Args:
            video_file (str)  : input video filename
            output_dir (str)  : output directory where video frames will be extracted
            frame_ext (str)   : extracted frame file format
            sampling (int)    : sampling rate -- extract one frame every given number of seconds.
                                Default=-1 for extracting all available frames
            verbose (bool)    : verbose mode
        """
        # Check if given video file exists -- abort otherwise
        if osp.exists(video_file):
            self.video_file = video_file
        else:
            raise FileExistsError('Video file {} does not exist.'.format(video_file))

        self.sampling = sampling

        # Create output directory for storing extracted frames
        self.output_dir = output_dir
        if not osp.exists(self.output_dir):
            os.makedirs(self.output_dir)

        # Get extracted frame file format
        self.frame_ext = frame_ext
        if frame_ext not in supported_frame_ext:
            raise ValueError("Not supported frame file format: {}".format(frame_ext))
        else:
            self.frame_ext = frame_ext

        # Get verbose flag
        self.verbose = verbose

        # Capture given video stream
        self.video = cv2.VideoCapture(self.video_file)

        # Get video fps
        self.video_fps = self.video.get(cv2.CAP_PROP_FPS)

        # Get video length in frames
        self.video_length = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
        if self.sampling != -1:
            self.video_length = self.video_length // self.sampling

        if self.verbose:
            print("#. Extract frames from video file: {}".format(self.video_file))
            print("  \\__Video FPS    : {}".format(self.video_fps))
            print("  \\__Video length : {} (frames)".format(self.video_length))

    def extract(self):
        # Get first frame
        success, frame = self.video.read()
        success = True
        frame_cnt = 0
        progress_step = 0
        progress_length = self.video_length if self.sampling == -1 else math.ceil(self.video_length / math.ceil(self.video_fps))
        while success:
            # Write current frame
            curr_frame_filename = osp.join(self.output_dir, "{:08d}{}".format(frame_cnt, self.frame_ext))
            cv2.imwrite(curr_frame_filename, frame)

            # Get next frame
            success, frame = self.video.read()

            if self.verbose:
                self.progress("  \\__Progress     : ", progress_length, progress_step + 1)

            if self.sampling != -1:
                frame_cnt += math.ceil(self.sampling * self.video_fps)
                self.video.set(1, frame_cnt)
            else:
                frame_cnt += 1
            progress_step += 1
            if progress_step >= progress_length:
                break

    @staticmethod
    def progress(msg, total, progress):
        bar_length, status = 20, ""
        progress = float(progress) / float(total)
        if progress >= 1.:
            progress, status = 1, "\r\n"
        block = int(round(bar_length * progress))
        block_symbol = u"\u2588"
        empty_symbol = u"\u2591"
        text = "\r{}{} {:.0f}% {}".format(msg, block_symbol * block + empty_symbol * (bar_length - block),
                                          round(progress * 100, 0), status)
        sys.stdout.write(text)
        sys.stdout.flush()


def main():
    # Set up a parser for command line arguments
    parser = argparse.ArgumentParser("Extract frames from videos")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--video', type=str, help='set video filename')
    group.add_argument('--dir', type=str, help='set videos directory')
    parser.add_argument('--sampling', type=int, default=-1,
                        help="extract 1 frame every args.sampling seconds (default: extract all frames)")
    parser.add_argument('--output_root', type=str, default='extracted_frames', help="set output root directory")
    parser.add_argument('-q', '--quite', action='store_true', help="set quite mode on")
    args = parser.parse_args()

    # Extract frames from a (single) given video file
    if args.video:
        # Setup video extractor for given video file
        video_basename = osp.basename(args.video).split('.')[0]
        # Check video file extension
        video_ext = osp.splitext(args.video)[-1]
        if video_ext not in supported_video_ext:
            raise ValueError("Not supported video file format: {}".format(video_ext))
        # Set extracted frames output directory
        output_dir = osp.join(args.output_root, '{}_frames'.format(video_basename))
        # Set up video extractor for given video file
        extractor = FrameExtractor(video_file=args.video, verbose=not args.quite, output_dir=output_dir)
        # Extract frames
        extractor.extract()

    # Extract frames from all video files found under the given directory (including all sub-directories)
    if args.dir:
        if not args.quite:
            print("#. Extract frames from videos under dir : {}".format(args.dir))
            if args.sampling == -1:
                print("#. Extract all available frames.")
            else:
                print("#. Extract one frame every {} seconds.".format(args.sampling))
            print("#. Store extracted frames under         : {}".format(args.output_root))
            print("#. Scan for video files...")

        # Scan given dir for video files
        video_list = []
        for r, d, f in walk(args.dir):
            for file in f:
                file_basename = osp.basename(file).split('.')[0]
                file_ext = osp.splitext(file)[-1]
                if file_ext in supported_video_ext:
                    video_list.append([osp.join(osp.relpath(r, args.dir), file),
                                       osp.join(osp.relpath(r, args.dir), "{}_frames".format(file_basename))])

        # Extract found video files
        for video_file in video_list:
            # Set up video extractor for given video file
            extractor = FrameExtractor(video_file=osp.join(args.dir, video_file[0]),
                                       output_dir=osp.join(args.output_root, video_file[1]),
                                       sampling=args.sampling,
                                       verbose=not args.quite)
            # Extract frames
            extractor.extract()


if __name__ == '__main__':
    main()
