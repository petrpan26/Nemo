from flask import Flask, jsonify, render_template
from scripts.meta_data import predefined_data
from scripts import core
from datetime import datetime

app = Flask(__name__)


@app.route('/upload_video/<video_id>', methods=['POST'])
def upload_video(video_id):
    core.download(video_id)
    return jsonify({'status': 200})


@app.route('/get_time/<video_id>/<caption>', methods=['GET'])
def get_time(video_id, caption):
    current = datetime.now()
    core.download(video_id)
    timestamp = core.get_timestamp(video_id, caption)
    print('Runtime: {} seconds'.format(datetime.now() - current))
    return jsonify({
        'video_id': video_id,
        'caption': caption,
        'timestamp': timestamp
    })


@app.route('/')
def root():
    return render_template('index.html')


app.run()
