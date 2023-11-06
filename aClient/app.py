from flask import Flask, request, jsonify, send_file, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    # This endpoint will receive audio from the user
    audio_file = request.files['audio_data']
    if audio_file:
        filename = 'user_audio.wav'
        audio_file.save(filename)

        # Here you could add logic to process the audio file and generate a response

        response_filename = 'response_audio.wav'
        # For this example, let's just echo back the same audio
        audio_file.save(response_filename)

        return send_file(response_filename, as_attachment=True)

    return jsonify({'error': 'No audio file'}), 400

if __name__ == '__main__':
    app.run(debug=True, threaded=True)