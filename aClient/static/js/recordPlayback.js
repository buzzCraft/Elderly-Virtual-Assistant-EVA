// JavaScript for handling audio recording and playback
let recordButton = document.getElementById('recordButton');
let audioPlayback = document.getElementById('audioPlayback');
let mediaRecorder;

recordButton.addEventListener('click', function() {
    if (mediaRecorder && mediaRecorder.state === "recording") {
        mediaRecorder.stop();
        recordButton.textContent = 'Record';
    } else {
        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(stream => {
                mediaRecorder = new MediaRecorder(stream);
                mediaRecorder.start();
                recordButton.textContent = 'Stop';

                let audioChunks = [];
                mediaRecorder.addEventListener("dataavailable", event => {
                    audioChunks.push(event.data);
                });

                mediaRecorder.addEventListener("stop", () => {
                    const audioBlob = new Blob(audioChunks, { 'type' : 'audio/wav' });
                    audioChunks = []; // Clear the chunks

                    const audioUrl = URL.createObjectURL(audioBlob);
                    audioPlayback.src = audioUrl;
                });
            });
    }
});