import time
import cv2 as cv
import mediapipe as mp
import os
import json

script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, "config.json")
with open(config_path, "r") as config_file:
    config = json.load(config_file)

acceptance_range_for_squats = config.get("acceptance_range_for_squats", 0)
is_show_squat_range_line = config.get("is_show_squat_range_line", True)
is_show_body_tracking_line = config.get("is_show_body_tracking_line", True)

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

video = cv.VideoCapture(0)

squats_counter = 0
reset_counter_gesture = False
squat_pose_detected = False
reset_timer_gesture = False
start_time = None

red_color = (0, 0, 255)
green_color = (0, 255, 0)
blue_color = (255, 0, 0)
white_color = (255, 255, 255)
black_color = (0, 0, 0)


def show_squats_counter(squats_counter):
    font = cv.FONT_HERSHEY_SCRIPT_SIMPLEX
    font_scale = 3
    font_thickness = 2
    counter_text = f"{squats_counter}"
    text_size = cv.getTextSize(counter_text, font, font_scale, font_thickness)[0]
    rect_x = 10
    rect_y = 10
    rect_width = text_size[0] + 20
    rect_height = text_size[1] + 20

    cv.rectangle(
        frame,
        (rect_x, rect_y),
        (rect_x + rect_width, rect_y + rect_height),
        black_color,
        thickness=cv.FILLED,
    )

    text_x = rect_x + 10
    text_y = rect_y + text_size[1] + 10

    cv.putText(
        frame,
        counter_text,
        (text_x, text_y),
        font,
        font_scale,
        red_color,
        font_thickness,
        cv.LINE_AA,
    )


def show_timer(timer):
    font = cv.FONT_HERSHEY_PLAIN
    font_scale = 2
    font_thickness = 2
    timer_text = f"{timer}"
    text_size = cv.getTextSize(timer_text, font, font_scale, font_thickness)[0]
    text_x = (frame.shape[1] - text_size[0]) // 2
    text_y = frame.shape[0] - 20

    rect_width = text_size[0] + 10
    cv.rectangle(
        frame,
        (text_x - 5, text_y - text_size[1] - 5),
        (text_x + rect_width, text_y + 5),
        black_color,
        thickness=cv.FILLED,
    )

    cv.putText(
        frame,
        timer_text,
        (text_x, text_y),
        font,
        font_scale,
        red_color,
        font_thickness,
        cv.LINE_AA,
    )


def timer_formatter(elapsed_time):
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    milliseconds = int((elapsed_time % 1) * 1000)
    timer_text = f"{minutes:02d}:{seconds:02d}:{milliseconds:03d}"
    return timer_text


while video.isOpened():
    success, frame = video.read()

    if not success:
        print("Ignoring empty video frame.")
        break

    rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

    result = pose.process(rgb_frame)

    pose_detected_with_confidence = (
        result.pose_landmarks
        and result.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP].visibility
        > 0.5
        and result.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].visibility
        > 0.5
    )

    if pose_detected_with_confidence:
        h, w, _ = frame.shape
        landmarks_pixel = [
            (int(landmark.x * w), int(landmark.y * h))
            for landmark in result.pose_landmarks.landmark
        ]

        if is_show_body_tracking_line:
            mp_drawing = mp.solutions.drawing_utils
            mp_drawing.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        hip_left_value = landmarks_pixel[mp_pose.PoseLandmark.LEFT_HIP.value]
        hip_right_value = landmarks_pixel[mp_pose.PoseLandmark.RIGHT_HIP.value]
        knee_left_value = landmarks_pixel[mp_pose.PoseLandmark.LEFT_KNEE.value]
        knee_right_value = landmarks_pixel[mp_pose.PoseLandmark.RIGHT_KNEE.value]

        squat_detected = hip_left_value[1] < (
            knee_left_value[1] - acceptance_range_for_squats
        ) and hip_right_value[1] < (knee_right_value[1] - acceptance_range_for_squats)

        if not squat_detected:
            show_squats_counter(squats_counter + 1)
            start_time = time.time()
        elif squat_detected:
            show_squats_counter(squats_counter)

        if squat_detected and not squat_pose_detected:
            squat_pose_detected = True
            squats_counter += 1
            start_time = None
        elif not squat_detected:
            squat_pose_detected = False

        if is_show_squat_range_line:
            knee_left_y = knee_left_value[1]
            knee_right_y = knee_right_value[1]
            range_line_y = (
                int((knee_left_y - acceptance_range_for_squats + knee_right_y) / 2)
                - acceptance_range_for_squats
            )
            cv.line(frame, (0, range_line_y), (w, range_line_y), red_color, 1)

        pose_reset_counter_detected = (
            result.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW].y
            < result.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].y
        )
        if pose_reset_counter_detected:
            reset_counter_gesture = True
            squats_counter = 0
            start_time = time.time()
        elif reset_counter_gesture:
            reset_counter_gesture = False

    if start_time is not None:
        elapsed_time = time.time() - start_time
        formatted_time = timer_formatter(elapsed_time)
        show_timer(formatted_time)
    else:
        show_timer("00:00:000")

    cv.namedWindow("Squat counter", cv.WINDOW_NORMAL)
    cv.imshow("Squat counter", frame)

    if cv.waitKey(1) & 0xFF == ord("q"):
        break

video.release()
cv.destroyAllWindows()
