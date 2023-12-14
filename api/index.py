from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.errorhandler(400)
def bad_request_error(error):
    return jsonify({'error': 'Bad Request', 'message': error.description}), 400

@app.errorhandler(401)
def unauthorized_error(error):
    return jsonify({'error': 'Unauthorized', 'message': error.description}), 401

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Not Found', 'message': 'The requested URL was not found on the server.'}), 404

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'error': 'Internal Server Error', 'message': error.description}), 500

@app.route("/prx")
def proxy_request():
    destination_url = request.args.get('destination')

    if not destination_url:
        return jsonify({'error': 'destination parameter is required'}), 400

    try:
        # Pass headers from the original request to the destination
        headers = request.headers
        response = requests.get(destination_url, headers=headers)
        
        if response.status_code == 200:
            return response.text
        else:
            return jsonify({'error': 'Failed to retrieve content from the destination'}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

@app.route("/prx2")
def proxy_request2():
    destination_url = request.args.get('destination')

    if not destination_url:
        return jsonify({'error': 'destination parameter is required'}), 400

    try:
        # Pass headers from the original request to the destination
        headers = request.headers
        response = requests.get(destination_url, headers=headers, allow_redirects=False)
        
        if response.status_code == 302:
            return response.headers['Location']
        else:
            return jsonify({'error': 'Failed to retrieve content from the destination'}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500
