// Text to Speech functionality
async function generateAudio() {
    const textInput = document.getElementById("inputText").value;
    const audioPlayer = document.getElementById("audioPlayer");

    if (textInput.trim() === "") {
        alert("Please enter some text to generate audio");
        return;
    }

    try {
        const response = await fetch("/tts", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ text: textInput })
        });

        const data = await response.json();

        if (data.audio_url && data.audio_url !== "Not Found") {
            audioPlayer.src = data.audio_url;
            audioPlayer.style.display = "block";
            audioPlayer.play();
        } else {
            alert("Failed to generate audio");
        }
    } catch (error) {
        console.error("Error generating audio:", error);
        alert("An error occurred while generating audio");
    }
}

// Echo Bot functionality
let mediaRecorder = null;
let audioStream = null;
let audioChunks = [];

const startButton = document.getElementById('startrecording');
const stopButton = document.getElementById('stoprecording');
const audioPlayer = document.getElementById('playback');
const uploadStatus = document.getElementById('uploadStatus');
const transcriptionContainer = document.getElementById('transcription-container');
const transcriptionText = document.getElementById('transcription-text');

function updateUIState(isRecording) {
    startButton.disabled = isRecording;
    stopButton.disabled = !isRecording;
    
    startButton.innerHTML = `<span>${isRecording ? 'Recording...' : 'Start Recording'}</span>`;
    if (isRecording) {
        startButton.classList.add('recording');
        transcriptionContainer.style.display = 'none';
        uploadStatus.textContent = 'Recording in progress...';
    } else {
        startButton.classList.remove('recording');
    }
}

async function transcribeAudio(audioBlob) {
    uploadStatus.textContent = 'Transcribing...';
    const formData = new FormData();
    formData.append('file', audioBlob, 'recording.webm');

    try {
        const response = await fetch('/transcribe/file', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            throw new Error(`Transcription failed: ${response.statusText}`);
        }

        const data = await response.json();
        transcriptionText.textContent = data.transcription;
        transcriptionContainer.style.display = 'block';
        uploadStatus.textContent = 'Transcription complete!';
    } catch (error) {
        console.error('Transcription error:', error);
        uploadStatus.textContent = 'Transcription failed.';
    }
}

async function startRecording() {
    try {
        audioStream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(audioStream);
        audioChunks = [];

        mediaRecorder.ondataavailable = event => {
            audioChunks.push(event.data);
        };

        mediaRecorder.onstop = async () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
            const audioUrl = URL.createObjectURL(audioBlob);
            audioPlayer.src = audioUrl;

            await transcribeAudio(audioBlob);
            
            audioStream.getTracks().forEach(track => track.stop());
        };

        mediaRecorder.start();
        updateUIState(true);
    } catch (error) {
        console.error('Error starting recording:', error);
        alert('Could not access microphone. Please grant permission and try again.');
        updateUIState(false);
    }
}

function stopRecording() {
    if (mediaRecorder && mediaRecorder.state === 'recording') {
        mediaRecorder.stop();
        updateUIState(false);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    startButton.addEventListener('click', startRecording);
    stopButton.addEventListener('click', stopRecording);
});
