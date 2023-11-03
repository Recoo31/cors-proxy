from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/proxy', methods=['GET'])
def proxy_request():
    destination_url = request.args.get('destination')
    
    if not destination_url:
        return jsonify({'error': 'destination parameter is required'}), 400
        
    try:
        response = requests.get(destination_url, allow_redirects=False)
        if response.status_code == 200:
            return response.content, response.status_code, response.headers.items()
        elif response.status_code == 302:
            # Handle redirection
            return jsonify({'error': 'Redirection is not allowed'}), 400
        else:
            return jsonify({'error': 'Failed to retrieve content from the destination'}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500
