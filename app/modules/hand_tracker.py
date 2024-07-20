import cv2
from enum import Enum
import mediapipe as mp
from dataclasses import dataclass, field

class HandLandMarks(Enum):
    HAND_BOTTOM = 0
    THUMB_TIP = 4
    INDEX_TIP = 8
    MIDDLE_BOTTOM = 9
    MIDDLE_TIP = 12
    RING_TIP = 16
    LITTLE_TIP = 20

@dataclass
class HandTracker:
    mp_hands: mp.solutions.hands = field(default_factory=lambda: mp.solutions.hands)
    mp_drawing: mp.solutions.drawing_utils = field(default_factory=lambda: mp.solutions.drawing_utils)
    hands: mp.solutions.hands.Hands = field(default_factory=lambda: mp.solutions.hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.5
    ))

    def get_landmarks(self, frame):
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_image)
        landmarks = results.multi_hand_landmarks if results.multi_hand_landmarks else None
        return landmarks

    def draw_hand_landmarks(self, hand_landmarks, frame):
        if hand_landmarks:
            for hand_landmark in hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    frame, hand_landmark, self.mp_hands.HAND_CONNECTIONS)

