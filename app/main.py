import cv2
from enum import Enum
import mediapipe as mp

class HandLandMarks(Enum):
    THUMP_TIP = 4
    INDEX_TIP = 8
    MIDDLE_TIP = 12
    RING_TIP = 16
    LITTLE_TIP = 20


# Constants
CAMERA_WIDTH, CAMERA_HEIGHT = 640, 480
EXIT_KEY = 27  # ESC key

# Initialize Mediapipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5
)

def set_camera(width=CAMERA_WIDTH, height=CAMERA_HEIGHT):
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    return cap

def process_frame(frame):
    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_image)
    bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                bgr_image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )
            process_landmarks(hand_landmarks, bgr_image)
    return bgr_image

def process_landmarks(hand_landmarks, frame):
    h, w, _ = frame.shape
    for index, landmark in enumerate(hand_landmarks.landmark):
        x = int(landmark.x * w)
        y = int(landmark.y * h)
        if index == HandLandMarks.INDEX_TIP.value:
            cv2.putText(frame, str(index), (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)


def show_video():
    cap = set_camera()
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        processed_frame = process_frame(frame)
        cv2.imshow('Hand Tracking', processed_frame)

        if cv2.waitKey(5) & 0xFF == EXIT_KEY:
            break

    cap.release()
    cv2.destroyAllWindows()

def main():
    show_video()

if __name__ == "__main__":
    main()
