from flask import Flask, request, jsonify
import os
import moviepy.editor as mp
from sent_transform import Searcher

app = Flask(__name__)


path_vid = 'vids/'
path_lab = 'labels/'
prefix_model = 'query: '

def load_files():
    js = {}
    file_labels = os.listdir(path_lab)
    for label in file_labels:
        vid_name = label.replace('.txt', '.mp4')
        js[label] = vid_name
    return js

dd = load_files()
finder_models = [Searcher(dd)]
def update_models(models, data):
    for model in models:
        model.update(data)

def most_vote_classify():
    pass

def get_single_answer(queries, models):
    return models[0].finder(queries)

@app.route('/endpoint', methods=['POST'])
def process_gif():
    uploaded_gif = request.files['uploaded_gif']
    gif_description = request.form.get('gif_description')
    gif_name = uploaded_gif.filename
    _name_lab = gif_name[:gif_name.find('.')] + '.txt'
    uploaded_gif.save(os.path.join(path_vid, gif_name))
    with open(os.path.join(path_lab, _name_lab), 'w') as fl:
        fl.write(prefix_model + gif_description)
    if '.gif' in gif_name:
        clip = mp.VideoFileClip(os.path.join(path_vid, gif_name))
        os.remove(os.path.join(path_vid, gif_name))
        gif_name = gif_name.replace('.gif', '.mp4')
        clip.write_videofile(os.path.join(path_vid, gif_name))
    dd[_name_lab] = os.path.join(path_vid, gif_name)
    update_models(finder_models, dd)
    return jsonify({"res": "true"})

@app.route('/find', methods=['POST'])
def process_query():
    text = request.form.get('text')
    relevant_labels = get_single_answer([prefix_model + text], finder_models)
    relevant_vids = [fl[0].split('.')[0] + '.mp4' for fl in relevant_labels]
    return jsonify({"videos": relevant_vids})

app.run(host='0.0.0.0')