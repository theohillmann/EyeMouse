import cv2
import pyautogui
from dataclasses import dataclass, field
from modules.hand_tracker import HandTracker
from modules.device_controller import DeviceController


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
    screen_config: ScreenConfig = field(default_factory=ScreenConfig.create)
    exit_key: int = 27
    hand_tracker: HandTracker = field(default_factory=HandTracker)
    device_controller: DeviceController = field(default_factory=DeviceController)

    def show_video(self):
        cap = self.set_camera()
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            hand_marks = self.hand_tracker.get_landmarks(frame)
            self.hand_tracker.draw_hand_landmarks(hand_marks, frame)
            if hand_marks:
                self.device_controller.control(frame, hand_marks[0])

            cv2.imshow('Hand Tracking', frame)

            if cv2.waitKey(5) & 0xFF == self.exit_key:
                break

        cap.release()
        cv2.destroyAllWindows()

    def set_camera(self):
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.screen_config.camera_width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.screen_config.camera_height)
        return cap
