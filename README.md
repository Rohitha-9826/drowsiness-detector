# Drowsiness Detector

A real-time drowsiness detector that uses a webcam to watch the user's eyes and
raises an alarm when they stay closed for too long. I built it to understand how
face landmark detection and simple geometry can be combined into a useful safety tool.

## How it works
1. OpenCV reads live frames from the webcam.
2. MediaPipe Face Mesh finds the face and returns 468 landmark points.
3. Six landmarks around each eye are used to calculate the Eye Aspect Ratio (EAR):

   EAR = (|p2 - p6| + |p3 - p5|) / (2 x |p1 - p4|)

   It is the eye's height divided by its width. It is high when the eye is open and
   drops close to zero when it closes. Because it is a ratio, it does not change
   when the user moves closer to or further from the camera.
4. If the average EAR of both eyes stays below the threshold for 1.5 seconds,
   a red alert banner is shown and a beep plays. A normal blink is far shorter,
   so it does not trigger the alert.

## Tech stack
- Python 3.10
- OpenCV (video capture and drawing)
- MediaPipe (face landmarks)

## How to run
1. `python -m venv venv`
2. `venv\Scripts\activate`
3. `pip install -r requirements.txt`
4. `python drowsiness_detector.py`
5. Press `q` to quit

## Settings
- `EAR_THRESHOLD = 0.22`: chosen from my own measurements (about 0.35 with eyes open, about 0.11 with eyes closed)
- `CLOSED_SECONDS = 1.5`: how long the eyes must stay closed before the alert

## Project files
- `drowsiness_detector.py`: the final program
- `webcam_test.py`, `eye_landmarks.py`, `ear.py`: earlier steps I built along the way (camera test, landmarks, EAR calculation)

## Limitations and next steps
- The alert sound uses `winsound`, so the sound works on Windows only
- The threshold was set from my own eyes; other users, glasses, or poor lighting may need a different value
- Tracks one face only
- Next: automatic per-user calibration, and head-pose (nodding) detection

## What I learned
I learned how face landmark models give points that can be turned into measurements with simple geometry, and why a ratio like EAR works better than raw distances. I also learned to choose a threshold from measured data and to use a time-based check instead of single frames, so normal blinks don’t trigger false alarms.