document.getElementById("sos-btn").addEventListener("click", function() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(sendSOS, handleGeoError);
    } else {
        alert("Geolocation not supported.");
    }
});

function sendSOS(position) {
    const latitude = position.coords.latitude;
    const longitude = position.coords.longitude;

    fetch("/send_sos", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ latitude, longitude })
    })
    .then(response => response.text())  // Use text first
    .then(text => {
        try {
            const data = JSON.parse(text);  // Convert to JSON safely
            if (data.success) {
                alert("SOS message sent successfully!");
            } else {
                alert("Error: " + data.error);
            }
        } catch (error) {
            console.error("Invalid JSON response:", text);
            alert("Server returned an unexpected response.");
        }
    })
    .catch(error => console.error("Request failed:", error));
}

function handleGeoError(error) {
    console.error("Geolocation error:", error.message);
    alert("Could not retrieve location: " + error.message);
}