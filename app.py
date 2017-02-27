from flask import Flask, jsonify

from dokidoki import get_doki


app = Flask(__name__)
app.config.from_object('config.ProductionConfig')

@app.route("/")
def doki():
    return jsonify(get_doki())

@app.route("/callback")
def callback():
    ''' Required for Anilist API authentication. No logic implemented. '''
    pass

if __name__ == '__main__':
    app.run()