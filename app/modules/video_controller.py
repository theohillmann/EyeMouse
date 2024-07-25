import cv2
import pyautogui
from dataclasses import dataclass, field
from modules.hand_tracker import HandTracker
from modules.device_controller import DeviceController
from screeninfo import get_monitors

@dataclass
class ScreenConfig:
    screen_width: int
    screen_height: int
    camera_width: float
    camera_height: float

    @classmethod
    def create(cls, screen_ratio: int = 1):
        screen_width, screen_height = pyautogui.size()
        camera_width = screen_width / screen_ratio
        camera_height = screen_height / screen_ratio
        return cls(screen_width, screen_height, camera_width, camera_height)


@dataclass
class VideoController:
    device_controller: DeviceController = field(init=False)
    screen_config: ScreenConfig = field(default_factory=ScreenConfig.create)
    exit_key: int = 27
    hand_tracker: HandTracker = field(default_factory=HandTracker)
    max_width: int = 0
    max_height:int = 0

    def __post_init__(self):
        self.set_monitors_limiters()
        self.device_controller = DeviceController(self.max_width, self.max_height)

    def process_frame(self):
        # cap = self.set_camera()
        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            hand_landmarks = self.hand_tracker.get_landmarks(frame)
            self.hand_tracker.draw_hand_landmarks(hand_landmarks, frame)
            if hand_landmarks:
                self.device_controller.control(frame, hand_landmarks[0])

            self.show_video(frame)
            if cv2.waitKey(5) & 0xFF == self.exit_key:
                break

        cap.release()
        cv2.destroyAllWindows()

    # def set_camera(self):
    #     cap = cv2.VideoCapture(0)
    #     cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.screen_config.camera_width)
    #     cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.screen_config.camera_height)
    #     return cap
    def set_monitors_limiters(self):
        for monitor in get_monitors():
            self.max_width += monitor.width
            self.max_height += monitor.height

    def show_video(self, frame):
        frame_with_rectangle_screen = self.draw_rectangle(frame)
        cv2.imshow('Hand Tracking', frame_with_rectangle_screen)

    def draw_rectangle(self, frame):
        DRAW_RATIO = 3.5
        frame_height, frame_width, _ = frame.shape
        BEGGIN_X = int(frame_width * 0.1)
        BEGGIN_Y = int(frame_height * 0.8)

        for monitor in get_monitors():
            start_point = (int((BEGGIN_X + monitor.x) / DRAW_RATIO), int((BEGGIN_Y + monitor.y) / DRAW_RATIO))
            end_point = (int((BEGGIN_X + monitor.x + monitor.width) / DRAW_RATIO), int((BEGGIN_Y + monitor.y + monitor.height)/ DRAW_RATIO))
            cv2.rectangle(frame, start_point, end_point, (255, 0, 0), 2)
        return frame