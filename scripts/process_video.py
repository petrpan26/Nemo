from captionbot import CaptionBot
import cv2
import os
import pickle
from datetime import datetime


def split_scene(video_id, filepath, frame_count):
    print('Splitting {}'.format(filepath))
    print(frame_count)
    start_time = datetime.now()
    dt = []
    # Playing video from file:
    cap = cv2.VideoCapture(filepath)

    try:
        image_path = 'data/{}/'.format(video_id)
        if not os.path.exists(image_path):
            os.makedirs(image_path)
        else:
            if os.path.isfile(image_path + 'video.data'):
                with open(image_path + 'video.data', 'rb') as cached_file:
                    return pickle.load(cached_file)
    except OSError:
        print('Error: Creating directory of data')

    if not cap.isOpened():
        cap.open('/Users/Thao/wd.mp4')

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    currentFrame = -1
    count = 0
    while(True):
        # Capture frame-by-frame

        ret, frame = cap.read()
        if (count % int(frame_count*fps) != 0):
            count += 1
            continue
        count += 1
        # Saves image of the current frame in jpg file
        if ret:
            name = image_path + str(currentFrame) + '.jpg'
            cv2.imwrite(name, frame)
            dt.append([name, count / fps])

            # To stop duplicate images
            currentFrame += 1
        else:
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    print('Splitting: {} seconds'.format(datetime.now() - start_time))
    with open(image_path + 'video.data', 'wb') as cached_file:
        pickle.dump(dt, cached_file)
    return dt


def captioning(video_id, scenes):
    print('Captioning {}'.format(video_id))
    start_time = datetime.now()
    c = CaptionBot()
    result = []
    cached_path = 'cached/{}.data'.format(video_id)
    if os.path.isfile(cached_path):
        with open(cached_path, 'rb') as cached_file:
            result = pickle.load(cached_file)
        for x in result:
            print('At {}: {}'.format(int(x['start_time']), x['caption']))
    else:
        for x in scenes:
            caption = c.file_caption(x[0])
            print('At {}: {}'.format(int(x[1]), caption))
            result.append({'start_time': x[1], 'caption': caption})
        with open(cached_path, 'wb') as cached_file:
            pickle.dump(result, cached_file)
    print('Captioning: {} seconds'.format(datetime.now() - start_time))
    return result


def get_data(video_id):
    return captioning(video_id, split_scene(video_id, 'downloaded/{}.mp4'.format(video_id), 1))
