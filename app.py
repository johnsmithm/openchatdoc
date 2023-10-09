from flask import Flask, request, session, jsonify, render_template
import os, sys, glob
from flask_swagger_ui import get_swaggerui_blueprint
import shutil

from chat.llm import get_response_llm
from embeddings.vector import process_files, index_files, FILES_DIR


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")


SWAGGER_URL = "/swagger"
API_URL = "/static/swagger.yaml"
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={"app_name": "Python-Flask-REST"})
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)


@app.route('/api/chat', methods=['POST'])
def chat_api():
    try:
        data = get_response_llm(request.json)

        return jsonify({"response": "success", "data": data })

    except Exception as error:
        return jsonify({"error": str(error)}), 400


@app.route('/api/delfile', methods=['DELETE'])
def delfile_api():
    try:
        file = request.args.get("fileid")
        if file is None or file.find('..')>=0:
            return jsonify({"error": "bad id file"}), 400

        if os.path.exists(FILES_DIR+'/'+file):
            shutil.rmtree(FILES_DIR+'/'+file)

        shutil.rmtree(FILES_DIR+'/all')

        index_files()

        return jsonify({"response": "success", "data": [] })
    except Exception as error:
        return jsonify({"error": str(error)}), 400


@app.route('/api/upload', methods=['POST'])
def upload_api():
    try:
        file = request.files.get("file")
        if file is None:
            return jsonify({"error": 'No files'}), 400
        if file.filename.split('.')[-1].lower() not in ['pdf','txt','doc','docx','xml','json','md']:
            return jsonify({"error": 'File extension not supported'}), 400

        data = process_files([file])

        return jsonify({"response": "success", "data": data })

    except Exception as error:
        return jsonify({"error": str(error)}), 400


@app.route('/chat', methods=['GET'])
def chat():
    body = {}

    return render_template('chat.html', body=body)


@app.route('/upload', methods=['GET'])
@app.route('/', methods=['GET'])
def upload_page():
    body = dict(files=[])

    files_dir = os.environ.get("FILES_DIR")
    for path in glob.glob(files_dir+'/*/*'):
        if path.split('.')[-1] in ['faiss','pkl']:
            continue
        body['files'] .append(dict(name=path.split('/')[-1], id=path.split('/')[-2]))

    return render_template('upload.html', body=body)

if __name__ == '__main__':
    
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 6006

    app.run(host='0.0.0.0', port=port, debug=True)