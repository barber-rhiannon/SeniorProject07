import dlib
import cv2
import csv
import os
import numpy as np

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("FacialLandmarking/shape_predictor_68_face_landmarks.dat")


def process_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    all_faces_features = []

    for face in faces:
        landmarks = predictor(gray, face)
        all_landmarks = np.array([[landmarks.part(n).x, landmarks.part(n).y] for n in range(68)])

        features = {
            'jawline': all_landmarks[0:17],
            'eyebrows': all_landmarks[17:27],
            'nose': all_landmarks[27:36],
            'eyes': all_landmarks[36:48],
            'lips': all_landmarks[48:68]
        }

        for feature in features.values():
            for x, y in feature:
                cv2.circle(img, (x, y), 3, (0, 255, 0), -1)

        all_faces_features.append(features)

    base_filename = os.path.basename(image_path)
    output_filename = "processed_" + base_filename
    output_path = os.path.join('Faciallandmarking/processed_images', output_filename)
    cv2.imwrite(output_path, img)

    return all_faces_features


def make_processed_photo():
    if not os.path.exists('FacialLandmarking/processed_images'):
        os.makedirs('FacialLandmarking/processed_images')

    image_directory = 'FacialLandmarking/original_images'
    image_paths = [os.path.join(image_directory, filename) for filename in os.listdir(image_directory) if filename.lower().endswith(('.png', '.jpg', '.jpeg'))]

    with open('image_paths.txt', 'w') as file:
        for path in image_paths:
            file.write(path + '\n')

    with open('facial_features.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Image', 'Feature', 'Landmark', 'X Coordinate', 'Y Coordinate'])

        for path in image_paths:
            all_faces_features = process_image(path)
            for features in all_faces_features:
                for feature_type, landmarks in features.items():
                    for index, (x, y) in enumerate(landmarks):
                        writer.writerow([path, feature_type, f'Landmark {index + 1}', x, y])

    print("Processing complete.")
    print("Mapping/landmarks are saved into facial_features.csv.")
    print("Processed images are saved into the processed_images directory.")
