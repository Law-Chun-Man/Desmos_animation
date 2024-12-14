import cv2
import os
from paths import desmos_frame

def frame_to_video(fps):
    # Set the folder containing the images and the output video file name
    image_folder = desmos_frame
    video_name = 'output_video.mp4'

    # Set frames per second
    fps = fps

    # Get a list of image file names in the folder
    images = [img for img in os.listdir(image_folder) if img.endswith((".png", ".jpg", ".jpeg"))]
    images.sort()  # Make sure images are sorted in the correct order

    # Read the first image to get width and height
    first_image_path = os.path.join(image_folder, images[0])
    frame = cv2.imread(first_image_path)
    height, width, layers = frame.shape

    # Define the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # For mp4 output
    video = cv2.VideoWriter(video_name, fourcc, fps, (width, height))

    # Loop through the images and add them to the video
    for image in images:
        img_path = os.path.join(image_folder, image)
        frame = cv2.imread(img_path)
        video.write(frame)

    # Release the video writer
    video.release()