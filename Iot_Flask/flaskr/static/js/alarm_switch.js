const switchElement = document.getElementById("alarmSwitch");
const statusLabel = document.getElementById("alarmStatus");

switchElement.addEventListener("change", function () {
    const newStatus = this.checked ? "ON" : "OFF";

    fetch('/execute_scrittura', {
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