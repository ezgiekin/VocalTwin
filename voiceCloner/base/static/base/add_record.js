const add_Start_Button = document.getElementById("add_start");
const add_Stop_Button = document.getElementById("add_stop");
const addButton = document.getElementById("add");

// Retrieve CSRF token for secure POST requests
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

const csrftoken = getCookie('csrftoken'); 

let gumStream; // Stream object for media
let rec; // Recorder object
let input; // MediaStreamSource for the recorder
let blob; // Variable to hold the recorded audio blob

const AudioContext = window.AudioContext || window.webkitAudioContext;
const audioContext = new AudioContext(); // Create an audio context

/**
 * Start recording audio from the user's microphone.
 */
function startRecording() {
    const constraints = { audio: true, video: false };

    add_Start_Button.disabled = true;
    add_Stop_Button.disabled = false;
    addButton.disabled = true;

    navigator.mediaDevices.getUserMedia(constraints).then(stream => {
        gumStream = stream;
        input = audioContext.createMediaStreamSource(stream);

        // Ensure the Recorder library is loaded
        if (typeof Recorder === 'undefined') {
            console.error("Recorder library not loaded.");
            return;
        }

        rec = new Recorder(input, { numChannels: 1 });
        rec.record();
    }).catch(err => {
        console.error("Error in getUserMedia: ", err);
        add_Start_Button.disabled = false;
        add_Stop_Button.disabled = true;
    });
}

/**
 * Stop recording audio and prepare for upload.
 */
function stopRecording() {
    add_Stop_Button.disabled = true;
    add_Start_Button.disabled = false;
    addButton.disabled = false;

    rec.stop();
    gumStream.getAudioTracks()[0].stop(); // Stop the audio track

    // Save the recorded blob and create an audio URL for immediate playback
    rec.exportWAV(recordedBlob => {
        blob = recordedBlob;
        console.log('Blob:', blob);

        const audioURL = window.URL.createObjectURL(blob);
        console.log('Audio URL:', audioURL);

        const player = document.getElementById("add_player");
        player.src = audioURL;
        player.load();  // Load the audio into the player
    });
}

/**
 * Upload the recording.
 */
function add() {
    if (!blob) {
        alert("No recording to upload.");
        return;
    }

    const formData = new FormData();
    formData.append("audio", blob, "recording.wav");

    fetch("", {
        method: "POST",
        body: formData,
        headers: {
            "X-CSRFToken": csrftoken // Add CSRF token for security
        }
    }).then(response => {
        if (response.ok) {
            location.reload(); // Reload page on successful upload
        } 
    })
}

// Event listeners for buttons
add_Start_Button.addEventListener("click", startRecording);
add_Stop_Button.addEventListener("click", stopRecording);
addButton.addEventListener("click", add);