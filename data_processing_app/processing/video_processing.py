import cv2 as opencv
import numpy as np
import face_recognition

from tensorflow import keras
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from data_processing_app.util import settings, visual_report
from data_processing_app.util.report_writer import ReportWriter


emotion_dict = settings.EMOTIONS_DICT


def _get_emotion(model, face_img):
    img = face_img.astype("float") / 255.0
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)
    predicted_class = np.argmax(model.predict(img))
    return predicted_class, emotion_dict.get(predicted_class, 'uknown')


def _crop_face_img(face_img, top, right, bottom, left):
    cropped_face = face_img[top:bottom, left:right]
    cropped_face = opencv.resize(cropped_face, (64, 64))
    return cropped_face


def run(webcam_view=False, live_preview=False, video_file=''):
    if webcam_view:
        vid_cap = opencv.VideoCapture(0)
    else:
        vid_cap = opencv.VideoCapture(f'media/recording1/{video_file}')

    if not vid_cap.isOpened():
        print('Failed to open video')
        return

    print('Start processing video...')

    model = load_model('data_processing_app/model/_mini_XCEPTION.102-0.66.hdf5', compile=False)
    process_frame = True
    start_time = 0
    period_emotions = []

    report_writer = ReportWriter('vid_em_report.csv')

    while vid_cap.isOpened():
        r, frame = vid_cap.read()

        if not r:
            print('No Frames')
            break

        current_time = int(vid_cap.get(opencv.CAP_PROP_POS_MSEC))
        # downscale video size for better performance
        downsized_frame = opencv.resize(frame, (0, 0), fx=0.25, fy=0.25)
        # skip frame for better performance
        if process_frame:   
            # convert image to RGB as this format is supported by face_recognition
            rgb = opencv.cvtColor(downsized_frame, opencv.COLOR_BGR2RGB)
            # transform image to grayscale for emotion prediction
            gray = opencv.cvtColor(downsized_frame, opencv.COLOR_BGR2GRAY)
            # detect faces on frame
            face_locs = face_recognition.face_locations(rgb, 1, 'hog')
            face_encs = face_recognition.face_encodings(rgb, face_locs)

        # process faces on frame
        for (top, right, bottom, left), face_enc in zip(face_locs, face_encs):
            crop_face = _crop_face_img(gray, top, right, bottom, left)
            c, emotion = _get_emotion(model, crop_face)

            if webcam_view == False:
                # write emnotion data each 5 seconds, later this value will depends no video duration
                if current_time - start_time >= 5000: 
                    start_time = current_time
                
                    current_time_pos = int(vid_cap.get(opencv.CAP_PROP_POS_MSEC)) / 1000
                    # save average emotion collected during 5 seconds
                    report_writer.write(current_time_pos, np.average(period_emotions))
                    
                    period_emotions.clear()
                else:
                    if emotion != 'uknown':
                        period_emotions.append(settings.EMOTIONS_SCORE.get(c))

            if webcam_view or live_preview:
                # restore back postions as frame was downscaled
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                font = opencv.FONT_HERSHEY_DUPLEX
                opencv.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 1)
                opencv.rectangle(frame, (left, bottom - 20), (right, bottom), (255, 255, 255), opencv.FILLED)
                opencv.putText(frame, emotion, (left + 6, bottom - 6), font, 0.5, (0, 0, 0), 1)

        process_frame = not process_frame

        if webcam_view or live_preview:
            opencv.imshow('Image', frame)

        if opencv.waitKey(1) == ord('q'):
            break

    if webcam_view == False:
        report_writer.close()
        visual_report.build()
        
    vid_cap.release()

    if webcam_view or live_preview:
        opencv.destroyAllWindows()


if __name__ == '__main__':
    run(False)