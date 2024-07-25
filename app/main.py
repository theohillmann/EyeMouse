from modules import VideoController


def main():
    video_display = VideoController()
    video_display.process_frame()

if __name__ == "__main__":
    main()