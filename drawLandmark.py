import face_recognition
import cv2
import numpy as np

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Initialize some variables
face_landmarks = []
face_names = []

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    #small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    #rgb_small_frame = small_frame[:, :, ::-1]
    rgb_small_frame = frame[:, :, ::-1]
    face_landmarks = face_recognition.face_landmarks(rgb_small_frame)
    parts = {'nose_bridge': (255,0,0),
            'nose_tip': (0,255,0),
            'top_lip': (0,0,255),
            'bottom_lip': (255,255,255),
            'left_eye': (128,128,0),
            'right_eye': (255,255,0),
            'left_eyebrow': (255,140,0),
            'right_eyebrow': (255,0,255),
            'chin': (0,255,255)}
    for face in face_landmarks:
        for name, points in face.items():
            for point in points:
                cv2.circle(frame,point, 2, color=parts[name], thickness=-1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()