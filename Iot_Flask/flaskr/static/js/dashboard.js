// Function to update switch state
function updateSwitchState(status) {
    const switchElement = document.getElementById("alarmSwitch");
    const statusLabel = document.getElementById("alarmStatus");

    if (status === "ON") {
        switchElement.checked = true;
        statusLabel.textContent = "Alarm is ON";
        statusLabel.classList.remove("text-danger");
        statusLabel.classList.add("text-success");
    } else if (status === "OFF") {
        switchElement.checked = false;
        statusLabel.textContent = "Alarm is OFF";
        statusLabel.classList.remove("text-success");
        statusLabel.classList.add("text-danger");
    }
}