import math
import cv2
import mediapipe as mp

RIGHT_EYE = [33, 160, 158, 133, 153, 144]
LEFT_EYE = [362, 385, 387, 263, 373, 380]


def get_points(landmarks, indices, w, h):
    return [(landmarks[i].x * w, landmarks[i].y * h) for i in indices]


def eye_aspect_ratio(p):
    vertical_1 = math.dist(p[1], p[5])
    vertical_2 = math.dist(p[2], p[4])
    horizontal = math.dist(p[0], p[3])
    return (vertical_1 + vertical_2) / (2.0 * horizontal)


mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:
        landmarks = results.multi_face_landmarks[0].landmark

        right = get_points(landmarks, RIGHT_EYE, w, h)
        left = get_points(landmarks, LEFT_EYE, w, h)

        ear = (eye_aspect_ratio(right) + eye_aspect_ratio(left)) / 2.0

        for x, y in right + left:
            cv2.circle(frame, (int(x), int(y)), 2, (0, 255, 0), -1)

        cv2.putText(frame, f"EAR: {ear:.2f}", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("EAR", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()