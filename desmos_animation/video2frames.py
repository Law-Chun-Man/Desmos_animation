import cv2
import os
from paths import jpg


def video_to_frames():
    def extract_frames(video_path, output_folder):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        video_capture = cv2.VideoCapture(video_path)

        frame_number = 0
        while True:
            success, frame = video_capture.read()
            if success:
                blurred_image = cv2.GaussianBlur(frame, (3, 3), 1.5)

                low_threshold = 50
                high_threshold = 150

                edges = cv2.Canny(blurred_image, low_threshold, high_threshold)
                # gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                frame_filename = os.path.join(output_folder, f'frame_{frame_number:04d}.jpg')
                cv2.imwrite(frame_filename, frame)
                frame_number += 1
            else:
                break

        video_capture.release()
        print("All frames extracted and saved.")


    video = ''
    folder_path = os.getcwd()
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) and (filename.lower().endswith('.mp4') or filename.lower().endswith('.mov') or filename.lower().endswith('.mkv')):
            video = filename

    extract_frames(video, jpg)
