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
console.log('Script loaded and initializing...');

let mediaRecorder = null;
let audioStream = null;
let audioChunks = [];

// Get DOM elements
const startButton = document.getElementById('startrecording');
const stopButton = document.getElementById('stoprecording');
const audioPlayer = document.getElementById('playback');
const uploadStatus = document.getElementById('uploadStatus');

console.log('DOM Elements:', {
    startButton: !!startButton,
    stopButton: !!stopButton,
    audioPlayer: !!audioPlayer,
    uploadStatus: !!uploadStatus
});

// Function to update UI state
function updateUIState(isRecording) {
    console.log('Updating UI state, isRecording:', isRecording);
    startButton.disabled = isRecording;
    stopButton.disabled = !isRecording;
    
    startButton.innerHTML = `<span class="button-icon">🎤</span>${isRecording ? 'Recording...' : 'Start Recording'}`;
    if (isRecording) {
        startButton.classList.add('recording');
    } else {
        startButton.classList.remove('recording');
    }
}


async function uploadAudioFile(audioBlob) {
    try {
        console.log('Starting upload...');
        uploadStatus.textContent = "Uploading...";
        uploadStatus.className = "upload-status uploading";

        const formData = new FormData();
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        const filename = `recording_${timestamp}.webm`;
        
        formData.append("file", audioBlob, filename);

        const response = await fetch("/upload", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error(`Upload failed: ${response.status}`);
        }

        const data = await response.json();
        console.log("Upload successful:", data);
        
        const fileSizeKB = (data.size / 1024).toFixed(1);
        uploadStatus.textContent = ` Uploaded: ${data.filename} (${fileSizeKB} KB)`;
        uploadStatus.className = "upload-status success";
        
        return data;
    } catch (error) {
        console.error("Upload failed:", error);
        uploadStatus.textContent = " Upload failed: " + error.message;
        uploadStatus.className = "upload-status error";
        throw error;
    }
}

// Function to handle recording start
async function startRecording() {
    console.log('Start recording clicked');
    try {
        console.log('Requesting microphone access...');
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        console.log('Microphone access granted');
        
        audioStream = stream;
        audioChunks = [];
        
        // Reset upload status
        uploadStatus.textContent = "Ready to record";
        uploadStatus.className = "upload-status";
        
        // Create media recorder
        mediaRecorder = new MediaRecorder(stream);
        console.log('MediaRecorder created:', mediaRecorder.state);

        // Handle data available event
        mediaRecorder.addEventListener('dataavailable', event => {
            console.log('Data available event:', event.data.size, 'bytes');
            audioChunks.push(event.data);
        });

        // Handle recording stop
        mediaRecorder.addEventListener('stop', async () => {
            console.log('Recording stopped, processing audio...');
            const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
            const audioUrl = URL.createObjectURL(audioBlob);
            audioPlayer.src = audioUrl;
            
            console.log('Audio processed and ready for playback');
            updateUIState(false);   
            
            // Stop all tracks
            audioStream.getTracks().forEach(track => {
                track.stop();
                console.log('Audio track stopped');
            });

            // Upload the audio file
            try {
                await uploadAudioFile(audioBlob);
            } catch (error) {
                console.error('Upload error:', error);
            }
        });

        // Start recording
        mediaRecorder.start();
        console.log('Recording started, MediaRecorder state:', mediaRecorder.state);
        updateUIState(true);

    } catch (error) {
        console.error('Error in startRecording:', error);
        alert('Could not access microphone - please ensure you have granted permission');
        updateUIState(false);
    }
}

// Function to handle recording stop
function stopRecording() {
    console.log('Stop recording clicked');
    if (mediaRecorder && mediaRecorder.state === 'recording') {
        console.log('Stopping recording...');
        mediaRecorder.stop();
    } else {
        console.log('MediaRecorder not active:', mediaRecorder?.state);
    }
}

// Add event listeners when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM Content Loaded, setting up event listeners');
    
    if (startButton && stopButton) {
        startButton.addEventListener('click', startRecording);
        stopButton.addEventListener('click', stopRecording);
        console.log('Event listeners attached successfully');
    } else {
        console.error('Required buttons not found in DOM');
    }
});

// Log if MediaRecorder is supported
console.log('MediaRecorder supported:', 'MediaRecorder' in window);