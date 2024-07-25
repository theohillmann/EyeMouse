# Hand Gesture Mouse Controller

## Description
The Hand Gesture Mouse Controller is a Python project that allows users to control their mouse using hand movements detected via a camera. The system interprets specific hand gestures to move the cursor, prepare for clicks, and perform click actions. 

## How It Works
- **Move Cursor:** Raise the index finger to control the mouse movement.
- **Prepare for Click:** Raise the pinky finger to stop the mouse and prepare for a click.
- **Click:** Raise and lower the middle finger to perform a click.
- **Scroll:** Raise both the middle finger and the index finger simultaneously to scroll up and down.

## Installation

### Prerequisites
- Python 3.8
- OpenCV
- Mediapipe

### Steps
1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/hand-gesture-mouse-controller.git
    cd hand-gesture-mouse-controller
    ```
2. Create a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
3. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage
1. Run the main script:
    ```sh
    python main.py
    ```
2. Make sure your camera is connected and working. The script will start detecting hand gestures to control the mouse.
