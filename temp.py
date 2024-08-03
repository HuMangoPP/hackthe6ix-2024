import cv2 as cv
import mediapipe as mp
import numpy as np

mp_face_detection = mp.solutions.face_detection

capture = cv.VideoCapture(0)
with mp_face_detection.FaceDetection(
  model_selection=1, min_detection_confidence=1) as face_detection:
  while capture.isOpened():
    success, image = capture.read()

    if not success:
      print("Cannot open camera")
      break
    image = cv.resize(image, (1280, 720))
    image.flags.writeable = False
    image_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)

    results = face_detection.process(image_rgb)

    image.flags.writeable = True
    image_bgr = cv.cvtColor(image_rgb, cv.COLOR_RGB2BGR)

    if results.detections:
      for detection in results.detections:
        key_points = np.array([(p.x, p.y) for p in detection.location_data.relative_keypoints]) 
        key_points_coords = np.multiply(key_points,[1280,720],).astype(int)
        for p in key_points_coords[0:1]:   
          cv.circle(image_bgr, p, 4, (255, 255, 255), 2)
          cv.circle(image_bgr, p, 2, (0, 0, 0), -1)
    cv.imshow('Face Detection', cv.flip(image_bgr, 1))
    if cv.waitKey(1) == ord('x'):
      break
capture.release()
cv.destroyAllWindows()