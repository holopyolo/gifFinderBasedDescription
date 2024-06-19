from flask import Flask, request, jsonify
import os
import moviepy.editor as mp
from sent_transform import Searcher

app = Flask(__name__)


path_vid = 'vids/'
path_lab = 'labels/'
dd = {
    "1.txt": "1.mp4",
    "2.txt": "2.mp4",
    "3.txt": "3.mp4",
    "4.txt": "4.mp4",
    "5.txt": "5.mp4",
}
model = Searcher(
    dd
)


@app.route('/endpoint', methods=['POST'])
def process_gif():
    uploaded_gif = request.files['uploaded_gif']
    gif_description = request.form.get('gif_description')
    gif_name = uploaded_gif.filename
    _name_lab = gif_name[:gif_name.find('.')] + '.txt'
    uploaded_gif.save(os.path.join(path_vid, gif_name))
    with open(os.path.join(path_lab, _name_lab), 'w') as fl:
        fl.write(gif_description)
    if '.gif' in gif_name:
        clip = mp.VideoFileClip(os.path.join(path_vid, gif_name))
        os.remove(os.path.join(path_vid, gif_name))
        gif_name = gif_name.replace('.gif', '.mp4')
        clip.write_videofile(os.path.join(path_vid, gif_name))
    dd[_name_lab] = os.path.join(path_vid, gif_name)
    model.update(dd)
    return jsonify({"res": "true"})

@app.route('/find', methods=['POST'])
def process_query():
    prefix = 'query: '
    text = request.form.get('text')
    
    relevant_labels = model.finder([prefix + text])
    relevant_vids = [fl[0].split('.')[0] + '.mp4' for fl in relevant_labels]
    return jsonify({"videos": relevant_vids})
print('not o')
app.run(host='0.0.0.0')
print('ok')