import os
from .meta_data import predefined_data
from .similarity import match
from .process_video import get_data


def get_timestamp(video_id, caption):
    print('Video ID: {}. Caption {}'.format(video_id, caption))
    if (video_id in predefined_data()):
        scene_data = predefined_data()[video_id]
    else:
        scene_data = get_data(video_id)
        for x in scene_data:
            print('At {}: {}'.format(int(x['start_time']), x['caption']))
    matched_idx = match(caption, [x['caption'] for x in scene_data])
    return int(scene_data[matched_idx]['start_time'])


def download(video_id):
    if not os.path.isfile('downloaded/{}.mp4'.format(video_id)):
        print('Downloading {}.mp4'.format(video_id))
        os.system(
            'youtube-dl -o downloaded/{}.mp4 https://www.youtube.com/watch?v={}'.format(video_id, video_id))
    print("Downloaded {}.mp4".format(video_id))
