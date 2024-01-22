import cv2 as cv
import mediapipe as mp
import os
import json

script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, 'config.json')
with open(config_path, 'r') as config_file:
    config = json.load(config_file)

acceptance_range_for_squats = config.get('acceptance_range_for_squats', 0)
show_squat_range_line = config.get('show_squat_range_line', False)

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

video = cv.VideoCapture(0)

squats_counter = 0
reset_counter_gesture = False
squat_pose_detected = False

red_color = (0, 0, 255)
green_color = (0, 255, 0)
blue_color = (255, 0, 0)

def show_squats_counter(squats_counter):
    cv.putText(
        frame,
        f"{squats_counter}",
        (10, 60),
        cv.FONT_HERSHEY_SCRIPT_SIMPLEX,
        2,
        green_color,
        2,
        cv.LINE_AA,
    )

while video.isOpened():
    success, frame = video.read()

    if not success:
        print("Ignoring empty video frame.")
        break

    rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

    result = pose.process(rgb_frame)

    pose_detected_with_confidence = (
        result.pose_landmarks
        and result.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP].visibility > 0.5
        and result.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].visibility > 0.5
    )

    if pose_detected_with_confidence:
        h, w, _ = frame.shape
        landmarks_pixel = [
            (int(landmark.x * w), int(landmark.y * h))
            for landmark in result.pose_landmarks.landmark
        ]

        connections = mp_pose.POSE_CONNECTIONS
        for connection in connections:
            start_point = landmarks_pixel[connection[0]]
            end_point = landmarks_pixel[connection[1]]
            cv.line(frame, start_point, end_point, green_color, 2)

        hip_left_value = landmarks_pixel[mp_pose.PoseLandmark.LEFT_HIP.value]
        hip_right_value = landmarks_pixel[mp_pose.PoseLandmark.RIGHT_HIP.value]
        knee_left_value = landmarks_pixel[mp_pose.PoseLandmark.LEFT_KNEE.value]
        knee_right_value = landmarks_pixel[mp_pose.PoseLandmark.RIGHT_KNEE.value]

        squat_detected = (
            hip_left_value[1] < (knee_left_value[1] - acceptance_range_for_squats) 
            and
            hip_right_value[1] < (knee_right_value[1] - acceptance_range_for_squats)
        )

        if not squat_detected:
            show_squats_counter(squats_counter + 1)
        elif squat_detected:
            show_squats_counter(squats_counter)

        if squat_detected and not squat_pose_detected:
            squat_pose_detected = True
            squats_counter += 1
        elif not squat_detected:
            squat_pose_detected = False

        if show_squat_range_line:
            knee_left_y = knee_left_value[1]
            knee_right_y = knee_right_value[1]
            range_line_y = int((knee_left_y - acceptance_range_for_squats + knee_right_y) / 2) - acceptance_range_for_squats
            cv.line(frame, (0, range_line_y), (w, range_line_y), red_color, 1)

        pose_reset_counter_detected = (
            result.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW].y
            < result.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].y
        )
        if pose_reset_counter_detected:
            reset_counter_gesture = True
            squats_counter = 0
        elif reset_counter_gesture:
            reset_counter_gesture = False

    cv.namedWindow("Squat counter", cv.WINDOW_NORMAL)
    cv.setWindowProperty("Squat counter", cv.WND_PROP_FULLSCREEN, cv.WINDOW_AUTOSIZE)
    cv.imshow("Squat counter", frame)

    if cv.waitKey(1) & 0xFF == ord("q"):
        break

video.release()
cv.destroyAllWindows()
