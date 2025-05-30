const switchElement = document.getElementById("alarmSwitch");
const statusLabel = document.getElementById("alarmStatus");


// Function to update switch and label text on the dashboard
function updateSwitchState(status) {
    const isOn = status === "ON";
    switchElement.checked = isOn;
    statusLabel.textContent = isOn ? "Alarm is ON" : "Alarm is OFF";
}

function fetchSwitchState() {
    fetch('/get_last_status')
        .then(response => response.json())
        .then(data => {
            if (data.status === "ON" || data.status === "OFF") {
                updateSwitchState(data.status);
            } else {
                console.warn("Unknown or missing status:", data.status);
            }
        })
        .catch(error => {
            console.error("Failed to fetch last status:", error);
        });
}


// Send command to alarm when user toggles switch
switchElement.addEventListener("change", function () {

    const newStatus = this.checked ? "ON" : "OFF";

    fetch('/execute_write', {
        method: 'POST',
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        updateSwitchState(newStatus);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});


// Fetch last switch status on page load
window.addEventListener("DOMContentLoaded", () => {
    fetchSwitchState()
});

setInterval(fetchSwitchState, 2000);