import cv2
import pyautogui
from dataclasses import dataclass, field
from modules import HandLandMarks


@dataclass
class DeviceController:
    hand_landmarks: list = field(init=False)

    def control(self, frame, hand_landmarks_object):
        self.hand_landmarks = hand_landmarks_object.landmark
        self.move_mouse(frame)
        # print(self.correct_hand_direction(self.is_finger_up(HandLandMarks.INDEX_TIP)))

    def correct_hand_direction(self, condition):
        return not (condition ^ self.is_hand_up())

    def is_finger_up(self, finger_tip):
        if finger_tip == HandLandMarks.THUMB_TIP:
            return
        finger_tip_value = finger_tip.value
        index_tip = self.hand_landmarks[finger_tip_value].y
        index_bottom = self.hand_landmarks[finger_tip_value - 3].y
        middle_top = self.hand_landmarks[finger_tip_value - 1].y
        middle_bottom = self.hand_landmarks[finger_tip_value - 2].y
        return index_tip < index_bottom and middle_top < middle_bottom

    def is_hand_up(self):
        hand_bottom = self.hand_landmarks[HandLandMarks.HAND_BOTTOM.value].y
        middle_bottom = self.hand_landmarks[HandLandMarks.MIDDLE_BOTTOM.value].y
        return hand_bottom > middle_bottom

    def move_mouse(self, frame):
        if self.is_finger_up(HandLandMarks.INDEX_TIP) and not self.is_finger_up(HandLandMarks.LITTLE_TIP):
            h, w, _ = frame.shape
            for index, landmark in enumerate(self.hand_landmarks):
                x = int(landmark.x * w)
                y = int(landmark.y * h)
                if index == HandLandMarks.INDEX_TIP.value:
                    pyautogui.moveTo(x, y, 0.1)