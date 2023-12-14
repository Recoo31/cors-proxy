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
        headers = {
            "host": "mobileservice-smarttv-lg.beinconnect.com.tr",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
            "accept-encoding": "gzip, deflate, br",
            "accept": "*/*",
            "connection": "keep-alive",
            "cookie": "uc=init=%22H4sIAAAAAAAEAIVRy27DIBD8F5%2brCAc3pr1hx24j5SHFVu4YtgoShgibVG3Vfy%2bRAolz6XFmdnd2dn%2bSJZwlh5VIXpMK59XLHNU4pyQjRUppTbJFmqOiKkmGFsnTtXrLevD1zYbu2%2fYQ6fbr5GntlApMYZkWU2pjBKgptRsOYAdptJ8Zh9XS9p%2fMQpTuO96ZFf%2bKD75Muw%2fGR2fBBmU17I0ZA2q4BdCN%2fI6d5cnRTk7RPEKjNfDR29%2fn3g3U8mNAt1x4hmeoy7LUByyVBD0%2b7H6FhZNKbF3f3bZ8A7M2nF2cLm96RgT7ULZfwzlc8vcPIXlwdsgBAAA%3d%22&uinf=0YUF6cc%2blKtJcY2N%2bYrPS5CROnstnaBgcZCz%2fhREPh7qUWTUphf5PgrL4%2bFHODlEYwpIcPjfrfn0hC5JYZYJDRXdgUcgwOF4hIhwmEY0SQZNayF7qZBVYZgCt09Z87C2VEL2wwCVbYiNRdjI0HZEtRxjddGeM33%2fpuNXepF0b3cDzCx%2fj3Kh7MNuyOXqFs3gNy6RNH52oWiF5HsqXhoag114MlGlpbNhxQAlOiVpaFhdq6fllz85q25AVNLTBSvqxvM2thrCtmMVJNM3Do6MsPMwVV4LtlAFjBPFN8tOYTAeA1IXExSb%2bQxC0V3ZjeWj; TS01f5b24d=0133743c616b8bc6a3d6365cacecb23d8e9e8d7a30194cb25c0d15184b099380ca4898e13a05c2380ca9c4548b68a09448f72c8e8b296f33b5186f19efe2a4754da7afb467"
        }
        response = requests.get(destination_url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return jsonify({'error': f'Failed to retrieve content from the destination \n {response.text}'}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500


@app.route("/prx2")
def proxy_request2():
    destination_url = request.args.get('destination')

    if not destination_url:
        return jsonify({'error': 'destination parameter is required'}), 400

    try:
        response = requests.get(destination_url, allow_redirects=False)
        if response.status_code == 302:
            return response.headers['Location']
        else:
            return jsonify({'error': 'Failed to retrieve content from the destination'}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500
