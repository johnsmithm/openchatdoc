import os
import shutil
import sys
import glob

from flask import Flask, request, jsonify, render_template
from flask_swagger_ui import get_swaggerui_blueprint

from chat.llm import get_response_llm
from embeddings.vector import process_files, index_files, FILES_DIR


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")


SWAGGER_URL = "/swagger"
API_URL = "/static/swagger.yaml"
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(SWAGGER_URL, API_URL, 
config={"app_name": "Python-Flask-REST"})
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)


@app.route('/api/chat', methods=['POST'])
def chat_api():
    """Handle chat requests via API, processing input and returning a response."""
    try:
        data = get_response_llm(request.json)
        return jsonify({"response": "success", "data": data})
    except ValueError as error:
        # Assuming ValueError might be a common exception to catch
        return jsonify({"error": str(error)}), 400
    except Exception as error:
        # Catching any other exceptions that weren't caught by the above
        return jsonify({"error": "An unexpected error occurred"+str(error)}), 500


@app.route('/api/delfile', methods=['DELETE'])
def delfile_api():
    """Handle delete file requests via API."""
    try:
        file = request.args.get("fileid")
        if file is None or file.find('..')>=0:
            return jsonify({"error": "bad id file"}), 400

        if os.path.exists(FILES_DIR+'/'+file):
            shutil.rmtree(FILES_DIR+'/'+file)

        shutil.rmtree(FILES_DIR+'/all')

        index_files()

        return jsonify({"response": "success", "data": [] })
    except ValueError as error:
        # Assuming ValueError might be a common exception to catch
        return jsonify({"error": str(error)}), 400
    except Exception as error:
        # Catching any other exceptions that weren't caught by the above
        return jsonify({"error": "An unexpected error occurred"+str(error)}), 500


@app.route('/api/upload', methods=['POST'])
def upload_api():
    """Handle file upload requests via API."""
    try:
        file = request.files.get("file")
        if file is None:
            return jsonify({"error": 'No files'}), 400
        if file.filename.split('.')[-1].lower() not in ['pdf','txt','doc','docx','xml','json','md']:
            return jsonify({"error": 'File extension not supported'}), 400

        process_files([file])

        return jsonify({"response": "success" })

    except ValueError as error:
        # Assuming ValueError might be a common exception to catch
        return jsonify({"error": str(error)}), 400
    except Exception as error:
        # Catching any other exceptions that weren't caught by the above
        return jsonify({"error": "An unexpected error occurred"+str(error)}), 500


@app.route('/chat', methods=['GET'])
def chat():
    """Handle chat requests and returning a html page."""
    body = {}

    return render_template('chat.html', body=body)

@app.route('/upload', methods=['GET'])
@app.route('/', methods=['GET'])
def upload_page():
    """Handle upload requests and returning a html page."""
    body = {"files":[]}

    files_dir = os.environ.get("FILES_DIR")
    for path in glob.glob(files_dir+'/*/*'):
        if path.split('.')[-1] in ['faiss','pkl']:
            continue
        body['files'] .append({"name": path.split('/')[-1], "id": path.split('/')[-2]})

    return render_template('upload.html', body=body)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        PORT = int(sys.argv[1])
    else:
        PORT = 6006

    app.run(host='0.0.0.0', port=PORT, debug=True)
