Enter file contents herefrom flask import Flask
from flask import request
from flask import render_template
from flask import jsonify
import json
import ast
import dbm


app = Flask(__name__)



@app.route('/')
def index():
    return render_template("index.html")
	
@app.route('/videos', methods = ['POST'])
def create_videoitem():
     if not request.json or not 'title' in request.json:
        abort(400)
     db = dbm.open('videodb', 'c')
     video = {
        'id': len(db.items()) + 1,
        'title': request.json['title'],
        'description': request.json.get('description'),
        'youtubelink': request.json.get('youtubelink')
     }
     db[str(len(db.items()) + 1)] = str(video);
     db.close()
     return get_videoitems()

@app.route('/videos', methods = ['GET'])
def get_videoitems():
    db = dbm.open('videodb', 'c')
    videos = []
    video = {}
    for v in db.values():
        videos.append(v.decode("utf-8"))
    return jsonify({'videos':videos})
	
@app.route('/videos/<int:video_id>', methods = ['GET'])
def delete_videoitem(video_id):
    db = dbm.open('videodb', 'c')
    del db[str(video_id)]
    return get_videoitems()

	
if __name__ == '__main__':
    app.run(debug = True)
