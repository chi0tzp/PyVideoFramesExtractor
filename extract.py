import sys
import os
from os import walk
import os.path as osp
import argparse
import cv2


class FrameExtractor:
    def __init__(self, video_file, output_root='extracted_frames', verbose=False):
        """Extract frames from video file and save them under a given output_dir.

        Args:
            video_file (str)  :
            output_root (str) :
            verbose (bool)    :
        """
        # Check if given video file exists -- abort otherwise
        if osp.exists(video_file):
            self.video_file = video_file
        else:
            raise FileExistsError('Video file {} does not exist.'.format(video_file))
        self.video_basename = osp.basename(video_file).split('.')[0]
        self.video_ext = osp.basename(video_file).split('.')[1]

        # Create output directory for storing extracted frames
        self.output_root = output_root
        self.output_dir = osp.join(self.output_root, osp.dirname(video_file), '{}_frames'.format(self.video_basename))
        if not osp.exists(self.output_dir):
            os.makedirs(self.output_dir)

        # Get verbose flag
        self.verbose = verbose

        # Capture given video stream
        self.video = cv2.VideoCapture(self.video_file)

        # Get video fps
        self.video_fps = self.video.get(cv2.CAP_PROP_FPS)

        # Get video length in frames
        self.video_length = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))

        if self.verbose:
            print("#. Extract frames from video file: {}".format(self.video_file))
            print("  \\__Video FPS    : {}".format(self.video_fps))
            print("  \\__Video length : {} (frames)".format(self.video_length))

    def extract(self):
        # Get first frame
        success, frame = self.video.read()
        curr_frame_num = 1
        success = True
        while success:
            # Write current frame
            curr_frame_filename = osp.join(self.output_dir, "{:08d}.jpg".format(curr_frame_num))
            cv2.imwrite(curr_frame_filename, frame)
            # Get next frame
            success, frame = self.video.read()
            if self.verbose:
                self.progress("  \\__Progress     : ", self.video_length, curr_frame_num)
            curr_frame_num += 1
        if self.verbose:
            print("")

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
    parser.add_argument('-o', '--output_root', type=str, default='extracted_frames', help="set output root directory")
    parser.add_argument('-q', '--quite', action='store_true', help="set quite mode on")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-v', '--video', type=str, help='set video filename')
    group.add_argument('-d', '--dir', type=str, help='set videos directory')
    args = parser.parse_args()

    # Extract frames from a (single) given video file
    if args.video:
        # Setup video extractor for given video file
        extractor = FrameExtractor(video_file=args.video, verbose=not args.quite, output_root=args.output_root)
        # Extract frames
        extractor.extract()

    # Extract frames from all video files found under the given directory (including all sub-directories)
    if args.dir:
        if not args.quite:
            print("#. Extract frames from videos in directory : {}".format(args.dir))
            print("#. Store extracted frames under            : {}".format(args.output_root))
            print("#. Scan for video files...")
        # Scan given dir for video files
        video_list = []
        for r, d, f in os.walk(args.dir):
            for file in f:
                video_list.append(os.path.join(r, file))
        # Extract found video files
        for video_file in video_list:
            # Setup video extractor for given video file
            extractor = FrameExtractor(video_file=video_file, verbose=not args.quite, output_root=args.output_root)
            # Extract frames
            extractor.extract()


if __name__ == '__main__':
    main()
