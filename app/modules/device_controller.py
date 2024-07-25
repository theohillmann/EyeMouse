import time

import cv2
import pyautogui
from dataclasses import dataclass, field
from modules import HandLandMarks


@dataclass
class DeviceController:
    max_width: int
    max_height: int
    hand_landmarks: list = field(init=False)
    is_clicking: bool = False
    middle_finger_up: bool = False
    initial_position_y: int = 0
    SCROLL_RATIO = 5

    def control(self, frame, hand_landmarks_object):
        self.hand_landmarks = hand_landmarks_object.landmark
        self.move_mouse(frame)
        self.click()
        self.scroll(frame)
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
        if (
            self.is_finger_up(HandLandMarks.INDEX_TIP)
            and not self.is_finger_up(HandLandMarks.LITTLE_TIP)
        ):
            h, w, _ = frame.shape
            for index, landmark in enumerate(self.hand_landmarks):
                # print(landmark.y)
                x = int(landmark.x * self.max_width)
                y = int(landmark.y * self.max_height)
                if index == HandLandMarks.INDEX_TIP.value:
                    pyautogui.moveTo(x, y)

    def click(self):
        if (
            self.is_finger_up(HandLandMarks.INDEX_TIP)
            and self.is_finger_up(HandLandMarks.LITTLE_TIP)
            and self.is_finger_up(HandLandMarks.MIDDLE_TIP)
            and self.is_clicking == False
        ):
            pyautogui.click()
            self.is_clicking = True

        if self.is_clicking and not self.is_finger_up(HandLandMarks.MIDDLE_TIP):
            self.is_clicking = False

    def scroll(self, frame):
        if (self.is_finger_up(HandLandMarks.INDEX_TIP)
            and self.is_finger_up(HandLandMarks.MIDDLE_TIP)
        ):
            if not self.middle_finger_up:
                self.middle_finger_up = True
                _, self.initial_position_y = pyautogui.position()
            self.scroll_movement(frame)
        else:
            self.middle_finger_up = False
    def scroll_movement(self, frame):
        _, current_postition_y = pyautogui.position()
        scroll_value = (self.initial_position_y - current_postition_y) / self.SCROLL_RATIO
        pyautogui.scroll(scroll_value)
        self.move_mouse(frame)
