/**
 * Get a cookie value by name.
 * @param {string} name - The name of the cookie to retrieve.
 * @returns {string|null} The value of the cookie or null if not found.
 */


function getCookie(name) {
    const cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                return decodeURIComponent(cookie.substring(name.length + 1));
            }
        }
    }
    return cookieValue;
}

/**
 * Filter table rows based on the search input.
 */
function myFunction() {
    const input = document.getElementById('recordSearcher').value.toLowerCase().trim();
    const table = document.getElementById('recordTable');
    const rows = table.getElementsByTagName('tr');

    for (let i = 1; i < rows.length; i++) {
        const columns = rows[i].getElementsByTagName('td');
        let found = false;

        for (let j = 0; j < columns.length; j++) {
            if (columns[j].textContent.toLowerCase().trim() === input) {
                found = true;
                break;
            }
        }
        rows[i].style.display = found ? "" : "none";
    }
}
 // Retrieve CSRF token for secure POST requests

let recorder; // Initialize recorder object
let chunks = []; // Array to hold audio chunks
let blob; // Variable to hold the recorded audio blob

// Browser compatibility
const URL = window.URL || window.webkitURL;
let gumStream; // Stream object for media
let rec; // Recorder object
let input; // MediaStreamSource for the recorder

const AudioContext = window.AudioContext || window.webkitAudioContext;
let audioContext; // Create an audio context

// Get HTML elements
const startButton = document.getElementById("start");
const stopButton = document.getElementById("stop");
const uploadButton = document.getElementById("upload");

/**
 * Start recording audio from the user's microphone.
 */
function startRecording() {
    const constraints = { audio: true, video: false };

    // Initialize the audioContext after user interaction
    if (!audioContext) {
        audioContext = new AudioContext();
    }

    startButton.disabled = true;
    stopButton.disabled = false;

    navigator.mediaDevices.getUserMedia(constraints).then(stream => {
        gumStream = stream;
        input = audioContext.createMediaStreamSource(stream);

        rec = new Recorder(input, { numChannels: 1 });
        rec.record();
    }).catch(err => {
        console.error("Error in getUserMedia: ", err);
        startButton.disabled = false;
        stopButton.disabled = true;
    });
}

/**
 * Stop recording audio and prepare for upload.
 */
function stopRecording() {
    stopButton.disabled = true;
    startButton.disabled = false;
    rec.stop();
    gumStream.getAudioTracks()[0].stop(); // Stop the audio track

    // Save the recorded blob and create an audio URL for immediate playback
    rec.exportWAV(recordedBlob => {
        blob = recordedBlob;

        // Create an audio URL from the blob and set it to the player
        const audioURL = window.URL.createObjectURL(blob);
        const player = document.getElementById("player");
        player.src = audioURL;
        player.load();  // Load the audio into the player
    });
}
/**
 * Upload the recorded audio to the server.
 */
function upload() {
    const formData = new FormData();

    // Check if there's a blob (recorded audio)
    if (blob) {
        formData.append("audio", blob, "recording.wav");
    }

    // Check if there's an uploaded file (from computer)
    const uploadedFile = document.getElementById('uploaded_audio').files[0];
    if (uploadedFile) {
        formData.append("uploaded_audio", uploadedFile);  // Use the same key "audio"
    }

    // If neither blob nor uploaded file exists, show an error and prevent the upload
    if (!blob && !uploadedFile) {
        alert("Please record or upload an audio file.");
        return;
    }

    // Append other form fields
    formData.append("name", document.getElementById('name').value);
    formData.append("gender", document.getElementById('gender').value);


    const csrftoken = getCookie('csrftoken'); 
    // Make the POST request
    fetch("", {
        method: "POST",
        body: formData,
        headers: {
            "X-CSRFToken": csrftoken  // Add CSRF token for security
        }
    }).then(response => {
        if (response.ok) {
            location.reload();  // Reload page on successful upload
        } else {
            console.error("Upload failed with status: ", response.status);
            alert("Error during file upload.");
        }
    }).catch(err => {
        console.error("Error during upload: ", err);
        alert("Error during file upload.");
    });
}

// Event listeners for buttons
startButton.addEventListener("click", startRecording);
stopButton.addEventListener("click", stopRecording);
uploadButton.addEventListener("click", upload);