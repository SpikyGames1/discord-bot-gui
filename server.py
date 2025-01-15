from flask import Flask, request, jsonify, Response, send_from_directory
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_file(path):
    return send_from_directory('.', path)

# Your existing proxy endpoint
@app.route('/proxy', methods=['OPTIONS', 'POST'])
def proxy():
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
        return response

    try:
        data = request.get_json()
        url = data.get('url')
        method = data.get('method', 'GET')
        headers = data.get('headers', {})
        payload = data.get('data', {})

        if not url:
            return jsonify({"error": "Missing 'url' in request body"}), 400

        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            json=payload if method != 'GET' else None
        )

        flask_response = Response(
            response.content,
            status=response.status_code,
            content_type=response.headers.get('content-type', 'application/json')
        )
        
        flask_response.headers.add('Access-Control-Allow-Origin', '*')
        return flask_response

    except Exception as e:
        print(f"Error in proxy: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
