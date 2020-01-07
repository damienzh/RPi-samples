import cv2
import numpy as np
import face_recognition as fr
import os
import pickle
import sys
import time


class FaceRecog:
    def __init__(self):
        self.known_faces_encodings = []
        self.known_faces_metadata = []
        self.known_faces_data_file = 'known_faces.dat'
        self.camera = None
        self.sample_image_path = os.path.join(os.path.dirname('__file__'), 'sample_image')
        if not os.path.exists(self.sample_image_path):
            os.mkdir(self.sample_image_path)

    def save_known_faces(self):
        """
        save all face registration data into file
        :return:
        """
        with open(self.known_faces_data_file, 'wb') as face_data_file:
            face_data = [self.known_faces_encodings, self.known_faces_metadata]
            pickle.dump(face_data, face_data_file)

    def load_known_faces(self):
        """
        Load known faces from file
        """
        try:
            with open(self.known_faces_data_file, 'rb') as face_data_file:
                self.known_faces_encodings, self.known_faces_metadata = pickle.load(face_data_file)
            print('{} known faces in database'.format(len(self.known_faces_encodings)))
        except FileNotFoundError as e:
            print("No known face data found")

    def register_new_face(self, face_encoding, face_image):
        """
        register a new face as known face
        :param face_encoding: 128-D numpy array of face encoding
        :param face_image: the image used to generate the face encoding
        """
        self.known_faces_encodings.append(face_encoding)
        self.known_faces_metadata.append({
            "face_image": face_image,
            "face_id": len(self.known_faces_metadata),
            "face_label": ''
        })

    def look_up_known_faces(self, face_encoding):
        """
        compare input face encoding with all known face encodings
        :param face_encoding: the face encoding to be compared
        :return: if the face is known then return its metadata, otherwise return None
        """
        metadata = None
        if len(self.known_faces_encodings) == 0:
            return metadata

        face_distances = fr.face_distance(self.known_faces_encodings, face_encoding)
        best_match_idx = np.argmin(face_distances)
        print('match index {}'.format(best_match_idx))
        best_fit = face_distances[best_match_idx]
        print('best match score {}'.format(best_fit))

        if best_fit < 0.45:
            metadata = self.known_faces_metadata[best_match_idx]
            print('I know you')
            return metadata

    def init_camera(self):
        """
        initialize usb camera
        """
        # self.camera = USBCamera(width=640, height=480, capture_width=640, capture_height=480, capture_device=0)
        self.camera = cv2.VideoCapture(0)
        time.sleep(1)

    def capture_face_frame(self, frame):
        """
        take frame from video stream then detect face in it
        :param frame: frame from video stream
        :return: face image cropped from stream frame
        """
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        small_frame_rgb = small_frame[:, :, ::-1]
        face_locations = fr.face_locations(small_frame_rgb)
        if len(face_locations) > 1:
            print('Too many faces, take another picture')
            return None
        elif len(face_locations) == 0:
            print('No face detected, take another picture')
            return None
        else:
            top, right, bottom, left = face_locations[0]
            face_image = small_frame_rgb[top:bottom, left:right]
            return face_image

    def generate_face_encoding(self, face_image):
        """
        resize cropped face image then generate 128-D face encoding for it
        :param face_image: face image cropped form original frame
        :return: face encoding generated for given image
        """
        img = cv2.resize(face_image, (150, 150))
        enc = fr.face_encodings(img)

        return enc[0]

    def save_face_img(self, image):
        """
        save captured frame into file
        :param image: frame captured by camera
        """
        image_list = [img for img in os.listdir(self.sample_image_path) if 'png' in img]
        new_image_name = 'test_image_{}.png'.format(len(image_list))
        cv2.imwrite(os.path.join(self.sample_image_path, new_image_name), image)
        print('{} saved'.format(new_image_name))

    def press_to_recognize(self):
        """
        press corresponding key to perform action
        """
        while True:
            ret, frame = self.camera.read()
            info1 = 'press q to quit'
            info2 = 'press a to recognize face'
            info3 = 'press s to save current frame'
            cv2.putText(frame, info1, (10, 430), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255))
            cv2.putText(frame, info2, (10, 450), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255))
            cv2.putText(frame, info3, (10, 470), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255))
            cv2.imshow('main', frame)
            k = cv2.waitKey(1)
            if k == ord('q'):
                self.save_known_faces()
                break
            elif k == ord('a'):
                face_image = self.capture_face_frame(frame)
                if face_image is not None:
                    cv2.imshow('face', face_image)
                    face_enc = self.generate_face_encoding(face_image)
                    face_metadata = self.look_up_known_faces(face_enc)
                    if not face_metadata:
                        self.register_new_face(face_enc, face_image)
                        print("I don't know you, register your face now")
            elif k == ord('s'):
                self.save_face_img(frame)


if __name__ == '__main__':
    # print(sys.version)
    f = FaceRecog()
    f.load_known_faces()
    f.init_camera()
    f.press_to_recognize()
    cv2.destroyAllWindows()
